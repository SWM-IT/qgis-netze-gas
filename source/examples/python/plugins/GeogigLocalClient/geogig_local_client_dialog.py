# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeogigLocalClientDialog
                                 A QGIS plugin
 Simplyfiedl client for GeoGig
                             -------------------
        begin                : 2017-10-20
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Markus Hesse / Mettenmeier GmbH
        email                : markus.hesse@mettenmeier.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import sqlite3

from functools import partial

from PyQt4 import QtGui, uic
from PyQt4.QtGui import (QProgressBar, QTextEdit)
from PyQt4.QtCore import *

#from PyQt4.QtGui import QTextEdit

from collections import defaultdict

#import qgis.utils
from qgis.utils import iface
from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtWidgets import (QMessageBox, 
                                 QTreeWidgetItem, 
                                 QMenu, 
                                 QInputDialog,
                                 QAbstractItemView, 
                                 QAction,
                                 QLabel)

#from qgis.PyQt.QtGui import QIcon, QMessageBox, QPixmap
from qgis.PyQt.QtGui import QIcon

from geogig import config
from geogig.geogigwebapi import repository
from geogig.repowatcher import repoWatcher
from geogig.geogigwebapi.repository import Repository
from geogig.tools.layertracking import getTrackingInfo
from geogig.tools.layers import namesFromLayer, hasLocalChanges
from geogig.tools.gpkgsync import (updateFeatureIds, getCommitId, applyLayerChanges)
from geogig.gui.dialogs.historyviewer import CommitTreeItemWidget, CommitTreeItem 

from GeogigLocalClient.tools.branchtracking import BranchesTracker
#from wx._grid import Grid_IsCurrentCellReadOnly

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'geogig_local_client_dialog_base.ui'))

pluginPath = os.path.dirname(__file__)

def icon(fileName):
    return QIcon(os.path.join(pluginPath, "ui", "resources", fileName))


class GeogigLocalClientDialog(QtGui.QDockWidget, FORM_CLASS):
    
    StrDefaultCommitComment = "Add comment for commit"
    MasterBranchName = "master"
    
    def __init__(self, parent=None):
        """Constructor."""
        super(GeogigLocalClientDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        
        self.branchtracking = BranchesTracker()
                
        self.setupUi(self)
        self.tbSync.setIcon(icon("sync_16.png"))
        self.tbPull.setIcon(icon("pull_16.png"))
        self.tbPush.setIcon(icon("push_16.png"))
        self.cbbServers.currentIndexChanged.connect(self.fillReposCombo)
        self.cbbRepos.currentIndexChanged.connect(self.fillBranchesList)
        
        self.tbSync.clicked.connect(self.syncSelectedBranch)
        self.tbPull.clicked.connect(self.pullMasterToCurrentBranch)
        self.tbPush.clicked.connect(self.pushCurrentBranchToMaster)
        
        self.tbPull.setEnabled(False)
        self.tbPush.setEnabled(False)
        
        self.branchesList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.branchesList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.branchesList.itemSelectionChanged.connect(self.branchSelected)
        self.branchesList.customContextMenuRequested.connect(self.showBranchedPopupMenu)
        
        self.updateClient()
    
    def showBranchedPopupMenu(self, point):
        item = self.branchesList.currentItem()
        self.menu = item.menu()
        point = self.branchesList.mapToGlobal(point)
        self.menu.popup(point)
        
    def updateClient(self):
        self.fillServersCombo()
        
    def fillServersCombo(self):
        self.cbbServers.clear()
        groups = repository.repoEndpoints.keys()
        self.cbbServers.addItems(groups)
        
    def fillReposCombo(self):
        self.cbbRepos.clear()
        serverName = self.cbbServers.currentText()
        serverRepos = repository.endpointRepos(serverName)
        serverReposNames = [repo.title for repo in serverRepos]
        self.cbbRepos.addItems(serverReposNames)
        
    def fillBranchesList(self):
        self.branchesList.clear()
        self.commitsList.clear()
        repo = self.getCurrentRepo()
        currentBranchName = self.getCurrentBranchName(repo)
        
        if repo:
            brancheNames = repo.branches()
            # "master is the only top level item    
            for branchName in brancheNames:
                if branchName == self.MasterBranchName:
                    topItem = BranchTreeItem(self, branchName, repo, branchName == currentBranchName)
                    self.branchesList.addTopLevelItem(topItem)
                    w = BranchTreeItemWidget(branchName, branchName == currentBranchName)
                    self.branchesList.setItemWidget(topItem, 0, w)
                    
                    if branchName == currentBranchName:
                        topItem.setSelected(True)
                    else:
                        topItem.setExpanded(True)
                    
                    break
                
            # Now the other branches. Thea are all children of master
            # FIXME: I would like to introduce a better hierarchy...
            for branchName in brancheNames:
                if branchName == self.MasterBranchName:
                    pass
                else:
                    # I assume, that branch names are unique inside one repository.
                    item = BranchTreeItem(self, branchName, repo, branchName == currentBranchName)
                    topItem.addChild(item)
                    w = BranchTreeItemWidget(branchName, branchName == currentBranchName)
                    self.branchesList.setItemWidget(item, 0, w)
                    
                    if branchName == currentBranchName:
                        item.setSelected(True)
                
            self.branchesList.resizeColumnToContents(0)  
            self.currentBranchChanged(currentBranchName)
            
    def getCurrentBranchName(self, repo):
        branchPath = self.branchtracking.getCurrentBranchPath(repo)
        
        if branchPath:
            return branchPath[-1]
        
    def currentBranchChanged(self, currentBranchName):
        if not currentBranchName or currentBranchName == "" or currentBranchName == self.MasterBranchName:
            self.tbPull.setEnabled(False)
            self.tbPush.setEnabled(False)
        else:
            self.tbPull.setEnabled(True)
            self.tbPush.setEnabled(True)          
    
    def branchSelected(self):
        self.commitsList.clear()
        selectedBranchName = self.selectedBranchName()
        if selectedBranchName:
            repo = self.getCurrentRepo()
            
            tags = defaultdict(list)
            for k, v in repo.tags().items():
                tags[v].append(k)
            
            commits = repo.log(until = selectedBranchName, limit = 100, path = None)
            for commit in commits:
                item = CommitTreeItem(commit)
                self.commitsList.addTopLevelItem(item)
                w = CommitTreeItemWidget(commit, tags.get(commit.commitid, []))
                self.commitsList.setItemWidget(item, 0, w)
            self.commitsList.resizeColumnToContents(0)
        
    def latestCommit(self, repo, branchName):
        commits = repo.log(until = branchName, limit = 1, path = None)
        if commits:
            return commits[0] 
                
    def syncSelectedBranch(self):
        """Synchronize the branch selected in the branch tree
        
        I check all required inputs and then run the sync over all layers available for this branch"""
        
        ok, repo = self.ensureCurrentRepo()
        if not ok:
            return
        
        # If a current branch is defined, take that one
        branchName = self.getCurrentBranchName(repo)
        
        if not branchName:
            ok, branchName = self.ensureSelectedBranch()
            if not ok:
                return       

        layers = self.layersInBranch(repo, branchName)        
        changedLayes = self.getChangedLayersOf(layers) 
        
        if changedLayes:
            commitComment, ok = QInputDialog.getText(self, 'Commit message',
                                                    'Enter a message:')
            if not ok:
                return  
            if commitComment == "":
                QMessageBox.warning(iface.mainWindow(), "No commit comment",
                                    "Please type in a comment for the commit.",
                                    QMessageBox.Ok)
                return
        else:
            commitComment = ""

        self.syncLayers(layers, branchName, commitComment)
        
        
    def gotoBranch(self, branchName):
        """Move to the selected branch
        
        I check all required inputs and then move all layers available for this branch to the selected branch.
        I take the head commit of the selected branch"""
        
        # Functionality mostly copied from layeractions.changeVersion:
        
        ok, repo = self.ensureCurrentRepo()
        if not ok:
            return
        
        ok, branchName = self.ensureSelectedBranch()
        if not ok:
            return 
        
        layers = self.layersInBranch(repo, branchName)
        changedLayes = self.getChangedLayersOf(layers) 
        
        if changedLayes:
            QMessageBox.warning(config.iface.mainWindow(), 'Cannot change branch',
                "One o more layers have local changes that would be overwritten. "
                "Either sync the branch or revert local changes "
                "before changing commit.",
                QMessageBox.Ok) 
        else:
            self.gotoBranchForLayers(repo, branchName, layers)
             
            if branchName == self.MasterBranchName:
                branchPath = [branchName]
            else:
                branchPath = [self.MasterBranchName, branchName]
                
            self.branchtracking.addBranchInfo(repo, branchPath)
            
            self.fillBranchesList()
            
    def createBranchFromBranch(self, branchName):
        ok, repo = self.ensureCurrentRepo()
        if not ok:
            return
        
        commit = self.latestCommit(repo, branchName)
        
        if commit:
            text, ok = QInputDialog.getText(self, 'Create New Branch',
                                            'Enter the name for the new branch:')
            if ok:
                repo.createbranch(commit.commitid, text.replace(" ", "_"))
                self.fillBranchesList()
                repoWatcher.repoChanged.emit(repo)

    def deleteBranch(self, branchName):
        ok, repo = self.ensureCurrentRepo()
        if not ok:
            return
        
        ret = QMessageBox.question(self, 'Delete Branch',
                    'Are you sure you want to delete this branch?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No)
        if ret == QMessageBox.No:
            return

        repo.deletebranch(branchName)
        self.fillBranchesList()
        repoWatcher.repoChanged.emit(repo)
        
    def pullMasterToCurrentBranch(self):
        repo = self.getCurrentRepo()
        currentBranchName = self.getCurrentBranchName(repo)
        self.mergeInto(currentBranchName, self.MasterBranchName)
    
    def pushCurrentBranchToMaster(self):
        repo = self.getCurrentRepo()
        currentBranchName = self.getCurrentBranchName(repo)
        self.mergeInto(self.MasterBranchName, currentBranchName)
    
    def mergeInto(self, mergeInto, branch):
        """ merge the branch names branch into the branch mergeInto"""
        # FIXME: The whole method is more or less copied from historyviewer.
        # Would be better to have this at one common point
        repo = self.getCurrentRepo()
        
        conflicts = repo.merge(branch, mergeInto)
        if conflicts:
            ret = QMessageBox.warning(iface.mainWindow(), "Conflict(s) found while syncing",
                                      "There are conflicts between local and remote changes.\n"
                                      "Do you want to continue and fix them?",
                                      QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.No:
                repo.closeTransaction(conflicts[0].transactionId)
                return

            dlg = ConflictDialog(conflicts)
            dlg.exec_()
            solved, resolvedConflicts = dlg.solved, dlg.resolvedConflicts
            if not solved:
                repo.closeTransaction(conflicts[0].transactionId)
                return
            for conflict, resolution in zip(conflicts, list(resolvedConflicts.values())):
                if resolution == ConflictDialog.LOCAL:
                    conflict.resolveWithLocalVersion()
                elif resolution == ConflictDialog.REMOTE:
                    conflict.resolveWithRemoteVersion()
                elif resolution == ConflictDialog.DELETE:
                    conflict.resolveDeletingFeature()
                else:
                    conflict.resolveWithNewFeature(resolution)
            user, email = config.getUserInfo()
            if user is None:
                return
            repo.commitAndCloseMergeAndTransaction(user, email, "Resolved merge conflicts", conflicts[0].transactionId)


        iface.messageBar().pushMessage("GeoGig", "Branch has been correctly merged",
                                              level=QgsMessageBar.INFO, duration=5)
        repoWatcher.repoChanged.emit(repo)

        
        
    def ensureCurrentRepo(self):
        repo = self.getCurrentRepo()
        if not repo:
            QMessageBox.warning(iface.mainWindow(), "No repository selected", 
                                "Please select the repository to sync with.",
                                QMessageBox.Ok) 
            return False, None
        else:
            return True, repo
        
        
    def getCurrentRepo(self):
        serverName = self.cbbServers.currentText()
        repoName = self.cbbRepos.currentText()
        
        if serverName == "" or repoName == "":
            exit
            
        serverRepos = repository.endpointRepos(serverName)
        
        for repo in serverRepos:
            if repo.title == repoName:
                return repo
        
    def ensureSelectedBranch(self):
        selectedBranchName = self.selectedBranchName()
        if selectedBranchName:
            return True, selectedBranchName
        else:
            QMessageBox.warning(iface.mainWindow(), "No branch selected", 
                                "Please select the branch to sync with.",
                                QMessageBox.Ok)
            return False, None
        
    def layersInBranch(self, repo, branchName):
        layerNames = repo.trees(branchName)
        allLayers  = iface.legendInterface().layers()
        
        # FIXME: The criterion storageType() == "GPKG" is not enough!
        # I should actually test, if that layer is managed via GeoGig!
        layers = []
        for layer in allLayers:
            if layer.name() in layerNames and layer.storageType() == "GPKG":
                layers.append(layer)
                
        return layers
        
        
    def syncLayers(self, layers, branchName, commitMessage):
        """Sync all given layers with the given message"""
        # FIXME: Handling of conflicts not implemented yet.
        self.prepareSync(len(layers))
        
        i = 0
        for layer in layers:
            self.progressMessageBar.setText("Synchronising branch {0}, Layer: {1}".format(branchName, layer.name()))
            self.syncLayer(layer, branchName, commitMessage)
            i += 1
            self.progressBar.setValue(i)
        
        self.finaliseSync()
        
        
    def syncLayer(self, layer, branchName, commitMessage):
        """Sync the given layer with the given message"""
        # FIXME: This is mainly copied form gpkgsync.syncLayer.
        # Here I only avoid the questions to the user about what 
        # branch and what commit message
        # FIXME2: Handling of conflicts not (well) implemented yet. 
        # FIXME3: I would like to handle this in one big commit over all layers, but that is not done yet.
        
        tracking = getTrackingInfo(layer)
        repo = Repository(tracking.repoUrl)
        filename, layername = namesFromLayer(layer)

        changes = hasLocalChanges(layer)
        
        if changes:
            ok = self.ensureDataModelIsUnchanged(filename, layername)
            if not ok:
                return 
            
            user, email = config.getUserInfo()
            # FIUXME: Message to user!
            if user is None:
                return
            
            # Now I try to send the changes from local gpkg to geogig server. 
            mergeCommitId, importCommitId, conflicts, featureIds = repo.importgeopkg(layer, branchName, commitMessage, user, email, True)
            
            if conflicts:
                QMessageBox.warning(iface.mainWindow(), "Error while syncing", 
                                    "There are conflicts between local and remote changes.\n"
                                    "Sync this layer separately via original GeoGig plugin.\n"
                                    "Layername: " + layer.name(),
                        QMessageBox.Ok)
                repo.closeTransaction(conflicts[0].transactionId)
                return
                
                # Original code from gpkgsync.syncLayer
                # For the moment I hoe I get no conflict
                #ret = QMessageBox.warning(iface.mainWindow(), "Error while syncing",
                #                          "There are conflicts between local and remote changes.\n"
                #                          "Do you want to continue and fix them?",
                #                          QMessageBox.Yes | QMessageBox.No)
                #if ret == QMessageBox.No:
                #    repo.closeTransaction(conflicts[0].transactionId)
                #    return
                #solved, resolvedConflicts = solveConflicts(conflicts)
                #if not solved:
                #    repo.closeTransaction(conflicts[0].transactionId)
                #    return
                #for conflict, resolution in zip(conflicts, list(resolvedConflicts.values())):
                #    if resolution == ConflictDialog.LOCAL:
                #        conflict.resolveWithLocalVersion()
                #    elif resolution == ConflictDialog.REMOTE:
                #        conflict.resolveWithRemoteVersion()
                #    elif resolution == ConflictDialog.DELETE:
                #        conflict.resolveDeletingFeature()
                #    else:
                #        conflict.resolveWithNewFeature(resolution)
                #repo.commitAndCloseMergeAndTransaction(user, email, "Resolved merge conflicts", conflicts[0].transactionId)
            
            updateFeatureIds(repo, layer, featureIds)
            try:
                applyLayerChanges(repo, layer, importCommitId, mergeCommitId)
            except:
                QgsMessageLog.logMessage("Database locked while syncing. Using full layer checkout instead", level=QgsMessageLog.CRITICAL)
                repo.checkoutlayer(tracking.geopkg, layername, None, mergeCommitId)

        else:
            # No change in local DB. So let's apply the changes from the GeoGig server to local DB.
            commitId = getCommitId(layer)
            headCommitId = repo.revparse(branchName)
            applyLayerChanges(repo, layer, commitId, headCommitId)
        
        
    def prepareSync(self, nbLayers):
        # Prepare the progressbar
        self.prepareProgressBar("Synchronising Layer", nbLayers)

    def prepareProgressBar(self, message, maxNb):
        # Prepare the progressbar
        progressMessageBar = iface.messageBar().createMessage(message)
        progress = QProgressBar()
        progress.setMaximum(maxNb)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)
        
        self.progressMessageBar = progressMessageBar
        self.progressBar = progress        
        
        
        
    def finaliseSync(self):
        # Update the list of commits
        self.branchSelected()
        
        # Remove the progress bar
        iface.messageBar().clearWidgets()
        
        # Show a nice success message to the user
        iface.messageBar().pushMessage("GeoGig", "Layers have been synchronized",
                                       level=QgsMessageBar.INFO,
                                       duration=5)
        
    def gotoBranchForLayers(self, repo, branchName, layers):
        self.prepareProgressBar("Moving to branch {0}".format(branchName), len(layers))
        
        i = 0
        for layer in layers:
            self.progressMessageBar.setText("Moving to branch {0}. Layer: {1}".format(branchName, layer.name()))
            
            tracking = getTrackingInfo(layer)
            repo.checkoutlayer(tracking.geopkg, layer.name(), None, branchName)
            layer.reload()
            layer.triggerRepaint()
            repoWatcher.layerUpdated.emit(layer)
            repoWatcher.repoChanged.emit(repo)

            i += 1
            self.progressBar.setValue(i)
            
         # Remove the progress bar
        iface.messageBar().clearWidgets()
        
        # Show a nice success message to the user
        iface.messageBar().pushMessage("GeoGig", "Move to branch " + branchName + " done",
                                       level=QgsMessageBar.INFO,
                                       duration=5)

                
    def ensureDataModelIsUnchanged(self, filename, layername):
        """I check, that the data model in the local GPKF file did not change between 
        last commit an now. If so, I show a message for the user and return false."""
        con = sqlite3.connect(filename)
        cursor = con.cursor()
        beforeAttrs = set(v[1] for v in cursor.execute("PRAGMA table_info('%s');" % layername))
        afterAttrs  = set(v[1] for v in cursor.execute("PRAGMA table_info('%s_audit');" % layername)
                         if v[1]not in ["audit_timestamp", "audit_op"])
        cursor.close()
        con.close()
        
        if beforeAttrs != afterAttrs:
            ret = QMessageBox.warning(iface.mainWindow(), "Cannot commit changes to repository",
                        "The structure of attributes table has been modified.\n"
                        "This type of change is not supported by GeoGig.",
                        QMessageBox.Ok)
            return False
        else:
            return True
        
    def selectedBranchName(self):
        if self.branchesList.selectedItems():
            return self.branchesList.selectedItems()[0].branchName
        
    def getChangedLayersOf(self, layers):
        changedLayers = []
        
        for layer in layers:
            changes = hasLocalChanges(layer)
            if changes:
                changedLayers.append(layer)
                
        return changedLayers 
    
        
class BranchTreeItem(QTreeWidgetItem):
    def __init__(self, owner, branchName, repo, isCurrent = False):
        QTreeWidgetItem.__init__(self)
        self.owner = owner
        self.branchName = branchName
        self.ref = branchName
        self.repo = repo

        #self.setIcon(0, branchIcon)
        self._commit = None
        self.current = isCurrent
        
    def menu(self):
        menu = QMenu()
        
        gotoAction = QAction("Goto this branch", menu)
        gotoAction.triggered.connect(partial(self.owner.gotoBranch, self.branchName))
        menu.addAction(gotoAction)
        
        createBranchAction = QAction("Create branch", menu)
        createBranchAction.triggered.connect(partial(self.owner.createBranchFromBranch, self.branchName))
        menu.addAction(createBranchAction)   
        
        deleteBranchAction = QAction("Delete branch", menu)
        deleteBranchAction.triggered.connect(partial(self.owner.deleteBranch, self.branchName))
        menu.addAction(deleteBranchAction)                
        
        return menu


class BranchTreeItemWidget(QLabel):
    def __init__(self, branchName, isCurrent):
        QTextEdit.__init__(self)
        self.setWordWrap(False)
        self.branchName = branchName
        self.isCurrent = isCurrent
        self.updateText()

    def updateText(self):
        size = self.font().pointSize()
        
        if self.isCurrent:
            text = ('<b><font style="font-size:%spt">%s</font></b>' %
                    (str(size + 1), self.branchName))
        else:
            text = self.branchName
            
        self.setText(text)
