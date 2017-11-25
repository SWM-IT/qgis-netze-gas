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
import zipfile

from qgis.PyQt.QtCore import pyqtSignal, QObject

class GeogigPackageReaderEngine(QObject):
    
    ARCHIVE_FOLDER_DATABASES = 'Databases'
    ARCHIVE_FOLDER_PROJECT   = 'Project'
    ARCHIVE_FOLDER_PLUGINS   = 'Plugins'
    ARCHIVE_FOLDER_CONFIG    = 'GeoigConfig'
    
    progressChanged = pyqtSignal(int, str)
    
    def __init__(self):
        QObject.__init__(self)
        self.archiveFile = None
        
    def run(self, fileName):
        """Do the creation of the package.
        
        :param fileName: Full file name of the package to be read.
        :type fileName: str
        """
        
        self._prepareArchiveFile(fileName)
        
        self.readDatabases()
        self.readProject()
        self.readConfig()
        self.readPlugins()
            
        self._closeArchiveFile()
        
        self.progressChanged.emit(100, "Done")
        
    def _prepareArchiveFile(sekf, fileName):
        pass
    
    def _closeArchiveFile(self):
        pass
        
    def readDatabases(self):
        pass
    
    def readProject(self):
        pass
        
    def readConfig(self):
        pass
    
    def readPlugins(self):
        pass

        
        
        