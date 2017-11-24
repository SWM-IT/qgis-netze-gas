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
import zipfile

from qgis.core import QgsProject

from geogig.tools.layertracking import (readTrackedLayers, tracked)

class GeogigPackageCreatorEngine(object):
    
    ARCHIVE_FOLDER_DATABASES = 'Databases'
    ARCHIVE_FOLDER_PROJECT   = 'Project'
    ARCHIVE_FOLDER_PLUGINS   = 'Plugins'
    ARCHIVE_FOLDER_CONFIG    = 'GeoigConfig'
    
    def __init__(self):
        self.archiveFile = None
        

    def Run(self, fileName, withDatabases=True, withProject=True, withConfiguration=True, withPlugins=True):
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
        
        self.prepareArchiveFile(fileName)
        
        if withDatabases:
            self.archiveDatabases()
            
        if withProject:
            self.archiveProject()
            
        self.closeArchiveFile()
        
    
    def prepareArchiveFile(self, fileName):
        """I create the zip file"""
        self.archiveFile = zipfile.ZipFile(fileName, mode='w', allowZip64 = True)
        
        
    def closeArchiveFile(self):
        """I clode the archive"""
        self.archiveFile.close()
        
        
    def archiveDatabases(self):
        """I zip all managed geo package files to the sub folder ARCHIVE_FOLDER_DATABASES of the new package zip"""
        for file in self.getTrackedPaths():
            self.archiveFile.write(file, 
                                   os.path.join(self.ARCHIVE_FOLDER_DATABASES, os.path.relpath(file, self.databaseFolder())), 
                                   compress_type = zipfile.ZIP_DEFLATED)
            
    def  databaseFolder(self):
        """I return the base path for all managed geo package files"""
        return os.path.join(os.path.expanduser('~'), 'geogig', 'repos')          
        
        
    def getTrackedPaths(self):
        """I return a list of all full file names with managed geo package files"""
        readTrackedLayers()
        trackedPaths = [layer.geopkg for layer in tracked]
        return trackedPaths

    def archiveProject(self):
        projectPath = QgsProject.instance().fileName()
        
        if projectPath:
            self.archiveFile.write(projectPath,
                                   os.path.join(self.ARCHIVE_FOLDER_PROJECT, os.path.basename(projectPath)),
                                   compress_type = zipfile.ZIP_DEFLATED)
        else:
            # No project file. Should be logged.
            pass
                                   
        
        
    def archiveFolder(self, sourceFolder, archiveFolder):
        for folder, subfolders, files in os.walk(sourceFolder):
            for file in files:
                self.archiveFile.write(os.path.join(folder, file), 
                                       os.path.join(archiveFolder, os.path.relpath(os.path.join(folder, file), sourceFolder)), 
                                       compress_type = zipfile.ZIP_DEFLATED)
 
    
    