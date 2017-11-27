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
        self.readProject()
        self.readConfig()
        self.readPlugins()
            
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
        #targetFolder = self._databaseFolder()
        targetFolder = "c:\\temp\\target\\databases"
        
        self._unzipFolder(self.ARCHIVE_FOLDER_DATABASES, targetFolder)
        
        #for fileInfo in self.archiveFile.infolist():
        #    if fileInfo.filename.startswith(self.ARCHIVE_FOLDER_DATABASES):
        #        self.archiveFile.extract(fileInfo, targetFolder)
        #        self._addFileSizeDone(fileInfo.file_size, fileInfo.filename)

    
    def readProject(self):
        targetFolder = "c:\\temp\\target\\project"

        self._unzipFolder(self.ARCHIVE_FOLDER_PROJECT, targetFolder)
        
        
    def readConfig(self):
        # FIXME
        targetFolder = "c:\\temp\\target\\config"
        
        self._unzipFolder(self.ARCHIVE_FOLDER_CONFIG, targetFolder)
        
        #for fileInfo in self.archiveFile.infolist():
        #   if fileInfo.filename.startswith(self.ARCHIVE_FOLDER_CONFIG):
        #        self.archiveFile.extract(fileInfo, targetFolder)
        #        self._addFileSizeDone(fileInfo.file_size, fileInfo.filename)
                        
    
    def readPlugins(self):
        # FIXME
        targetFolder = "c:\\temp\\target\\plugins"
        
        self._unzipFolder(self.ARCHIVE_FOLDER_PLUGINS, targetFolder)
        
        #for fileInfo in self.archiveFile.infolist():
        #    if fileInfo.filename.startswith(self.ARCHIVE_FOLDER_PLUGINS):
        #        self.archiveFile.extract(fileInfo, targetFolder)
         #       self._addFileSizeDone(fileInfo.file_size, fileInfo.filename)
                
    def _unzipFolder(self, sourcePath, targetFolder):
        """I unzip all files below sourcePath from the zip file and store them below targetFoleder"""
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
                    
                self._addFileSizeDone(fileInfo.file_size, fileInfo.filename)
        

    def _addFileSizeDone(self, value, progressString):
        self.fileSizeDone += value
        progress = round(self.fileSizeDone/float(self.fileSizeSum) * 100)
        self.progressChanged.emit(progress, progressString)
        
    
    def _databaseFolder(self):
        # Actually I would like to use geogig.tools.utils.parentReposFolder
        # But it may be, that the plugin geogig is not yet installed.
        # Thus I use the default folder for geogig geo packages files.
        return os.path.join(os.path.expanduser('~'), 'geogig', 'repos')
        
        
        
        
        