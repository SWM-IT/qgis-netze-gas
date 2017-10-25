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

from PyQt4 import QtGui, uic

from PyQt4.QtGui import QProgressBar
from PyQt4.QtCore import *

from collections import defaultdict

#import qgis.utils
from qgis.utils import iface
from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtWidgets import (QMessageBox, QTreeWidgetItem)

#from qgis.PyQt.QtGui import QIcon, QMessageBox, QPixmap
from qgis.PyQt.QtGui import QIcon

from geogig import config
from geogig.geogigwebapi import repository
from geogig.geogigwebapi.repository import Repository
from geogig.tools.layertracking import getTrackingInfo
from geogig.tools.layers import namesFromLayer, hasLocalChanges
from geogig.tools.gpkgsync import (updateFeatureIds, getCommitId, applyLayerChanges)
from geogig.gui.dialogs.historyviewer import CommitTreeItemWidget, CommitTreeItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'geogig_local_client_dialog_base.ui'))

pluginPath = os.path.dirname(__file__)

def icon(fileName):
    return QIcon(os.path.join(pluginPath, "ui", "resources", fileName))


#class GeogigLocalClientDialog(QtGui.QDialog, FORM_CLASS):
class GeogigLocalClientDialog(QtGui.QDockWidget, FORM_CLASS):
    
    StrDefaultCommitComment = "Add comment for commit"
    
    def __init__(self, parent=None):
        """Constructor."""
        super(GeogigLocalClientDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
                
        self.setupUi(self)
        self.tbSync.setIcon(icon("sync_16.png"))
        self.tbPull.setIcon(icon("pull_16.png"))
        self.tbPush.setIcon(icon("push_16.png"))
        self.cbbServers.currentIndexChanged.connect(self.fillReposCombo)
        self.cbbRepos.currentIndexChanged.connect(self.fillBranchesList)
        self.tbSync.clicked.connect(self.syncSelectedBranch)
        self.branchesList.itemClicked.connect(self.branchSelected)
        self.commitText.textChanged.connect(self.commitTextChanged)
        self.commitText.setTextColor(QtGui.QColor("grey"))
        self.updateClient()
    
        
    def updateClient(self):
        self.fillServersCombo()
        self.revertCommitText()
        
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
        
        if repo:
            brancheNames = repo.branches()
            # "master is the only top level item    
            for branchName in brancheNames:
                if branchName == "master":
                    topItem = BranchTreeItem(branchName, repo)
                    self.branchesList.addTopLevelItem(topItem)
                    break
                
            # Now the other branches. Thea are all children of master
            # FIXME: I would like to introduce a better hierarchy...
            for branchName in brancheNames:
                if branchName == "master":
                    pass
                else:
                    item = BranchTreeItem(branchName, repo)
                    topItem.addChild(item)
                
            self.branchesList.resizeColumnToContents(0)  
            
    
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
        
            
    
    def getCommitText(self): 
        return self.commitText.document().toPlainText()
    
    def ensureCommitComment(self):
        commitComment = self.getCommitText()
        
        if commitComment == "" or commitComment == self.StrDefaultCommitComment:
            ret = QMessageBox.warning(iface.mainWindow(), "No commit comment",
                        "Please type in a comment for the commit.",
                        QMessageBox.Ok)
            return False, ""
        else:
            return True, commitComment
        
            
    def commitTextChanged(self):
        if self.commitText.document().toPlainText() == self.StrDefaultCommitComment:
            self.commitText.setTextColor(QtGui.QColor("grey"))
        else:
            self.commitText.setTextColor(QtGui.QColor("black"))
        
    def revertCommitText(self):
        self.commitText.setTextColor(QtGui.QColor("grey"))
        self.commitText.document().setPlainText(self.StrDefaultCommitComment)

        
    def syncSelectedBranch(self):
        ok, repo = self.ensureCurrentRepo()
        if not ok:
            return
        
        ok, branchName = self.ensureSelectedBranch()
        if not ok:
            return       
        
        ok, commitComment = self.ensureCommitComment()
        if not ok:
            return  

        layers = self.layersInBranch(repo, branchName)
        self.syncLayers(layers, branchName, commitComment)
        
        
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
        progressMessageBar = iface.messageBar().createMessage("Synchronising Layer")
        progress = QProgressBar()
        progress.setMaximum(nbLayers)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)
        
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
        
class BranchTreeItem(QTreeWidgetItem):
    def __init__(self, branchName, repo):
        QTreeWidgetItem.__init__(self)
        self.branchName = branchName
        self.ref = branchName
        self.repo = repo
        #self.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        self.setText(0, branchName)
        #self.setIcon(0, branchIcon)
        self._commit = None
        
    
