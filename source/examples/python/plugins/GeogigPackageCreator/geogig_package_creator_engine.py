# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Geogig Package Creator Engine
                                 Helper do the actual packaging
                             -------------------
        begin                : 2017-11-17
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
import zipfile

from qgis.core import QgsProject
from qgis.PyQt.QtCore import pyqtSignal, QObject

from geogig.tools.layertracking import (readTrackedLayers, tracked)
from geogig.tools.utils import (parentReposFolder)

class GeogigPackageCreatorEngine(QObject):
    
    ARCHIVE_FOLDER_DATABASES = 'Databases'
    ARCHIVE_FOLDER_PROJECT   = 'Project'
    ARCHIVE_FOLDER_PLUGINS   = 'Plugins'
    ARCHIVE_FOLDER_CONFIG    = 'GeoigConfig'
    
    progressChanged = pyqtSignal(int, str)
    
    
    def __init__(self):
        QObject.__init__(self)
        self.archiveFile = None
        

    def run(self, fileName, withDatabases=True, withProject=True, withConfiguration=True, withPlugins=True):
        """Do the creation of the package.
        
        :param fileName: Full file name of the package to be created
        :type fileName: str
        
        :param withDatabases: If true, the databases maintained by Geogig will be added to the package.
        :type withDatabases: bool
        
        :param withProject: If true, the QGIS project file will be added to the package.
        :type withProject: bool

        :param withConfiguration: If true, the Geogig configuration will be added to the package.
        :type withConfiguration: bool
        
        :param withPlugins: If true, the Geogig plugins will be added to the package.
        :type withPlugins: bool        
        """
        
        self._prepareArchiveFile(fileName)
        
        
        self.progressChanged.emit(0, "Storing databases")

        if withDatabases:
            self.archiveDatabases()
            
        self.progressChanged.emit(90, "Storing Project")
            
        if withProject:
            self.archiveProject()
            
        if withConfiguration:
            self.archiveConfig()
            
        if withPlugins:
            self.archivePlugins()
            
        self._closeArchiveFile()
        
        self.progressChanged.emit(100, "Done")
        
    
    def _prepareArchiveFile(self, fileName):
        """I create the zip file"""
        self.archiveFile = zipfile.ZipFile(fileName, mode='w', allowZip64 = True)
        
        
    def _closeArchiveFile(self):
        """I clode the archive"""
        self.archiveFile.close()
        
        
    def archiveDatabases(self):
        """I zip all managed geo package files to the sub folder ARCHIVE_FOLDER_DATABASES of the new package zip"""
        nbDatabase = 0
        nbDone     = 0
        for file in self._getTrackedPaths():
            if os.path.exists(file): nbDatabase += 1 
        
        for file in self._getTrackedPaths():
            self.progressChanged.emit(-1, "File: " + os.path.basename(file))
            self._doArchiveFile(file, os.path.join(self.ARCHIVE_FOLDER_DATABASES, 
                                                  os.path.dirname(os.path.relpath(file, self._databaseFolder()))))
            nbDone += 1 
            progress = round(nbDone/float(nbDatabase) * 100)
            self.progressChanged.emit(progress, "File: " + os.path.basename(file))
                                

    def archiveProject(self):
        projectPath = QgsProject.instance().fileName()
        
        if projectPath:
            self._doArchiveFile(projectPath, self.ARCHIVE_FOLDER_PROJECT)
        else:
            # No project file. Should be logged.
            pass
                     
    
    def archiveConfig(self):
        """ Archive all configuration files"""
        configFolder = self._geogigConfigFolder()
        
        for configFile in ['repositories', 'trackedlayers', 'trackedBranches']:
            self._doArchiveFile(os.path.join(configFolder, configFile), self.ARCHIVE_FOLDER_CONFIG)
            
    def archivePlugins(self):
        for pluginName in ['qgiscommons2', 'geogig', 'GeogigLocalClient']:
            pluginFolder = os.path.dirname(sys.modules[pluginName].__file__)
            self._archiveFolder(pluginFolder, self.ARCHIVE_FOLDER_PLUGINS)
            
            
    def  _databaseFolder(self):
        """I return the base path for all managed geo package files"""
        return parentReposFolder()          
        
        
    def _getTrackedPaths(self):
        """I return a list of all full file names with managed geo package files"""
        readTrackedLayers()
        #trackedPaths = [layer.geopkg for layer in tracked]
        #return trackedPaths
        return [layer.geopkg for layer in tracked]

        
    def _geogigConfigFolder(self):
        """ Folder with geogig configuration files"""
        return os.path.join(os.path.expanduser('~'), 'geogig')
        
    def _archiveFolder(self, sourceFolder, archiveFolder):
        for folder, subfolders, files in os.walk(sourceFolder):
            for file in files:
                self.archiveFile.write(os.path.join(folder, file), 
                                       os.path.join(archiveFolder, os.path.relpath(os.path.join(folder, file), os.path.dirname(sourceFolder))), 
                                       compress_type = zipfile.ZIP_DEFLATED)
                
        
    def _doArchiveFile(self, sourceFile, targetFolder):
        """Archive the given file to the given folder in the archive
        
        If the file does not exists, it is skipped"""
        
        if not os.path.exists(sourceFile):
            # FIXME: Some logging?!
            return 
        
        self.archiveFile.write(sourceFile,
                               os.path.join(targetFolder, os.path.basename(sourceFile)),
                               compress_type = zipfile.ZIP_DEFLATED)
        
 
    
    