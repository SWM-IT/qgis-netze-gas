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
import io
import sys
import zipfile

import json
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder

from qgis.core import QgsProject
from qgis.PyQt.QtCore import pyqtSignal, QObject

from geogig.tools.layertracking import (readTrackedLayers, TrackedLayer, Encoder)
from geogig.tools.utils import (parentReposFolder)

import geogig.tools.layertracking 

def decoder(jsonobj):
    if 'source' in jsonobj:
        return TrackedLayer(jsonobj['source'],
                           jsonobj['repoUrl'])
    else:
        return jsonobj

class GeogigPackageCreatorEngine(QObject):
    
    ARCHIVE_FOLDER_DATABASES = 'Databases'
    ARCHIVE_FOLDER_PROJECT   = 'Project'
    ARCHIVE_FOLDER_PLUGINS   = 'Plugins'
    ARCHIVE_FOLDER_CONFIG    = 'GeoigConfig'
    
    progressChanged = pyqtSignal(int, str)
    
    
    def __init__(self):
        QObject.__init__(self)
        self.archiveFile = None
        self.doneMarkers = []
        

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
        
        self.doneMarkers = []
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
            self.progressChanged.emit(progress, "Compressing file: " + os.path.basename(file))
                                

    def archiveProject(self):
        projectPath = QgsProject.instance().fileName()
        
        if projectPath:
            self._doArchiveProjectFile(projectPath, self.ARCHIVE_FOLDER_PROJECT)
        else:
            # No project file. Should be logged.
            pass
                     
    
    def archiveConfig(self):
        """ Archive all configuration files"""
        configFolder = self._geogigConfigFolder()
        
        # Prepare trackedlayers file: Here I have typically user specific paths.
        # To avoid changing that on target machine, I change them to absolute,
        # static paths.
        currentPath = self._databaseFolder().lower()
        targetPath  = self._targetDatabaseFolder().lower()
        
        filename = os.path.join(configFolder, "trackedlayers")
        if os.path.exists(filename):
            
            trackInfos = self._readTrackedLayerFile(filename)
            
            for trackInfo in trackInfos:
                trackInfo.geopkg = trackInfo.geopkg.lower().replace(currentPath, targetPath)
                trackInfo.source = trackInfo.source.lower().replace(currentPath, targetPath)
                
                
            trackedString= json.dumps(trackInfos, cls = Encoder)
                        
            self.archiveFile.writestr(os.path.join(self.ARCHIVE_FOLDER_CONFIG, 'trackedlayers'),
                                      trackedString,
                                      compress_type = zipfile.ZIP_DEFLATED)
                        
        # The other config files I can add to the zip unchanged.
        for configFile in ['repositories', 'trackedBranches']:
            self._doArchiveFile(os.path.join(configFolder, configFile), self.ARCHIVE_FOLDER_CONFIG)
            
    def archivePlugins(self):
        for pluginName in ['qgiscommons2', 'geogig', 'GeogigLocalClient']:
            pluginFolder = os.path.dirname(sys.modules[pluginName].__file__)
            self._archiveFolder(pluginFolder, self.ARCHIVE_FOLDER_PLUGINS)
            
            
    def  _databaseFolder(self):
        """I return the base path for all managed geo package files"""
        return parentReposFolder() 
    
    def _targetDatabaseFolder(self):
        """Folder where I want to store the databases on the target machine
        
        Note, that I try to avoid a user specific folder. That way I can prepare 
        the trackedlayers file and need not customize it on target side"""
        return os.path.join(os.getenv('PROGRAMDATA'), 'geogig', 'repos')         
        
        
    def _getTrackedPaths(self):
        """I return a list of all full file names with managed geo package files"""
        readTrackedLayers()

        # Note: It is important to call tracked as a qualified name and do not import the global:
        # An import of the global in fact created a copy of it and I do not see the change by readTrackedLayers().
        return [layer.geopkg for layer in geogig.tools.layertracking.tracked]

        
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
        
 
    def _doArchiveProjectFile(self, sourceFile, targetFolder):
        """Archive the given file to the given folder in the archive
        
        If the file does not exists, it is skipped"""
        
        if not os.path.exists(sourceFile):
            # FIXME: Some logging?!
            return 
        
        
        # Prepare QGis project file: Here I have typically user specific paths.
        # To avoid changing that on target machine, I change them to absolute,
        # static paths.
        currentPath = self._databaseFolder().lower()
        targetPath  = self._targetDatabaseFolder()
        
        new_lines = []
        with io.open(sourceFile, "r", encoding="utf-8") as f:
            for line in f:
                if currentPath in line.lower():
                    new_lines.append(line.lower().replace(currentPath, targetPath))
                elif '<prop k="name" v=' in line:
                    new_lines.append(self._archiveStyleMarker(line, sourceFile))
                else:
                    new_lines.append(line)
                                    
        self.archiveFile.writestr(os.path.join(targetFolder, os.path.basename(sourceFile)),
                                  "".join(new_lines).encode('utf-8'),
                                  compress_type = zipfile.ZIP_DEFLATED)
        
        
    def _archiveStyleMarker(self, line, projectFile):
        """I check, if the line contains a SVG file or similar things for the style.
        
        If so, I put the related SVG to the archive file and change the line accordingly.
        I return either the original line or a changed one"""
        
        # I assume something like this
        # <prop k="name" v="../QGis/Gas-Demo/svg/sp_ga/g_hausanschluss.position_hausanschluss_in_betri.0.svg"/>
        # So I try to find the path to the SVG file between two defined marks 
        
        startMark = 'v="'
        endMark   = '"/>'
        
        projectName = os.path.splitext(os.path.basename(projectFile))[0]
        markerDir   = os.path.join(self.ARCHIVE_FOLDER_PROJECT, projectName, 'Markers')
        
        if (not startMark in line) or (not endMark in line): 
            return line
        
        path = line[line.index(startMark) + len(startMark):line.index(endMark)]
        
        if not os.path.isabs(path):
            fileName = os.path.join(os.path.dirname(projectFile), path)
        else:
            fileName = path
        
        
        if not os.path.exists(fileName):
            return line
        
        if not (fileName in self.doneMarkers):
            self._doArchiveFile(fileName, markerDir)
            self.doneMarkers.append(fileName)
        
        newFileName = os.path.join('.', projectName, 'Markers', os.path.basename(fileName))
        return line.replace(path, newFileName) 

            
    def _readTrackedLayerFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            
        trackInfo = JSONDecoder(object_hook = decoder).decode("\n".join(lines))
            
        return trackInfo
    
    
         
