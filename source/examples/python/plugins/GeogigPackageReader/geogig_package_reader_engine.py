# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Geogig Package Reader Engine
                                 Helper do the actual packaging
                             -------------------
        begin                : 2017-11-25
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
import sys
import shutil
import zipfile

from PyQt4.QtCore import QSettings, QVariant, QFileInfo

import qgis.utils
from qgis.core import QgsApplication, QgsProject

from qgis.PyQt.QtCore import pyqtSignal, QObject
from __builtin__ import True

class GeogigPackageReaderEngine(QObject):
    
    ARCHIVE_FOLDER_DATABASES = 'Databases'
    ARCHIVE_FOLDER_PROJECT   = 'Project'
    ARCHIVE_FOLDER_PLUGINS   = 'Plugins'
    ARCHIVE_FOLDER_CONFIG    = 'GeoigConfig'
    
    progressChanged = pyqtSignal(int, str)
    
    def __init__(self):
        QObject.__init__(self)
        self.archiveFile  = None
        self.fileSizeSum  = 0
        self.fileSizeDone = 0
        
    def run(self, fileName):
        """Do the creation of the package.
        
        :param fileName: Full file name of the package to be read.
        :type fileName: str
        """
        
        self.progressChanged.emit(0, "Reading package")
        
        if not self._prepareArchiveFile(fileName):
            return
        
        self._getFileSizeSum()
        self.fileSizeDone = 0
        
        self.readDatabases()
        self.readConfig()
        self.readPlugins()
        self.readProject()
            
        self._closeArchiveFile()
        
        self.progressChanged.emit(100, "Done")
        
    def _prepareArchiveFile(self, fileName):
        """I open the zip file"""
        
        if zipfile.is_zipfile(fileName):
            self.archiveFile = zipfile.ZipFile(fileName, mode='r', allowZip64 = True)
            return True
        else:
            return false
        
    def _getFileSizeSum(self):
        """I sum up the files sizes of all files in the archive file and store it in fileSizeSum"""
        self.fileSizeSum = 0
        
        for info in self.archiveFile.infolist():
            self.fileSizeSum += info.file_size

    
    def _closeArchiveFile(self):
        """I clode the archive"""
        self.archiveFile.close()
        
    def readDatabases(self):
        """I unzip the files from Databases and store them in the gegig databases folder"""
        targetFolder = self._databaseFolder()       
        self._unzipFolder(self.ARCHIVE_FOLDER_DATABASES, targetFolder)

    
    def readProject(self):
        targetFolder = self._defaultProjectFolder()
        anyProject   = self._unzipFolder(self.ARCHIVE_FOLDER_PROJECT, targetFolder)
        
        if anyProject:
            self.progressChanged.emit(-1, 'Opening project file')
            
            projectFile = os.listdir(targetFolder)[0]
            project     = QgsProject.instance() 
            project.read(QFileInfo(os.path.join(targetFolder, projectFile)))        
        
        
    def readConfig(self):
        targetFolder = self._geogigConfigFolder()        
        self._unzipFolder(self.ARCHIVE_FOLDER_CONFIG, targetFolder)
                                
    
    def readPlugins(self):
        targetFolder = self._pluginsFolder()        
        anyPlugin    = self._unzipFolder(self.ARCHIVE_FOLDER_PLUGINS, targetFolder)
        
        self.progressChanged.emit(-1, 'Setting up plugins')
        
        if anyPlugin:
            # Activate plugins
            for pluginName in ['qgiscommons2', 'geogig', 'GeogigLocalClient']:
                qgis.utils.loadPlugin(pluginName)

            for pluginName in ['geogig', 'GeogigLocalClient']:
                qgis.utils.startPlugin(pluginName)

            settings=QSettings()
            for pluginName in ['geogig', 'GeogigLocalClient']:
                settings.setValue('PythonPlugins/' + pluginName, True)
                
            # I import here, because it may be, the plugin has just been unzipped.
            from geogig.gui.dialogs.navigatordialog import navigatorInstance
            navigatorInstance.setVisible(False)
            
            from geogig.tools.layertracking import (readTrackedLayers)
            readTrackedLayers()
                
                
    def _unzipFolder(self, sourcePath, targetFolder):
        """I unzip all files below sourcePath from the zip file and store them below targetFolder.
        
        I return True, if there was anything to unzip"""
        anythingUnzipped = False
        
        for fileInfo in self.archiveFile.infolist():
            if fileInfo.filename.startswith(sourcePath):
                # I cannot simply use self.archiveFile.extract(fileInfo, targetFolder) because 
                # that would produce folder with names like self.ARCHIVE_FOLDER_PLUGINS
                # To get rid of the beginning folders in the zip, I need to figure out the 
                # target path myself etc. 
                filename   = os.path.relpath(fileInfo.filename, sourcePath)
                targetfile = os.path.join(targetFolder, filename)
                if not os.path.exists(os.path.dirname(targetfile)):
                    os.makedirs(os.path.dirname(targetfile))
                source = self.archiveFile.open(fileInfo)
                target = file(targetfile, "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
                
                anythingUnzipped = True
                self._addFileSizeDone(fileInfo.file_size, fileInfo.filename)
                
        return anythingUnzipped
        

    def _addFileSizeDone(self, value, progressString):
        """I add value to self.fileSizeDone and emit a progressChanged signal accordingly"""
        self.fileSizeDone += value
        progress = round(self.fileSizeDone/float(self.fileSizeSum) * 100)
        self.progressChanged.emit(progress, progressString)
        
    
    def _databaseFolder(self):
        """Folder for the databases on the target machine
        
        Note, that this folder can difer from geogig.tools.utils.parentReposFolder
        because that is a configuration that points per default to the users home 
        directory. But we want to avoid user specific directories. That would imply, 
        we need to modify also the configuration (mainly trackedlayers file) pointing 
        to the databases.""" 
        return os.path.join(os.getenv('PROGRAMDATA'), 'geogig', 'repos')
        
    def _pluginsFolder(self):
        """Folder where the plugins shall be stored"""
        # FIXME: Is use qgisSettingsDirPath because I can influence it by --configpath
        # parameter on QGis start and it seems QGis searches actually there for plugins.
        # But is this really the right way? There should be something more explicit!?
        return os.path.join(QgsApplication.qgisSettingsDirPath(), 'python', 'plugins')
    
    def _geogigConfigFolder(self):
        """ Folder with geogig configuration files"""
        return os.path.join(os.path.expanduser('~'), 'geogig')
    
    def _defaultProjectFolder(self):
        """Folder to store the QGis project file in."""
        return os.path.join(os.getenv('PROGRAMDATA'), 'geogig', 'qgis')
        
        
        
        