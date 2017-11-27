# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeogigPackageCreatorDialog
                                 A QGIS plugin
 Plugin to create a package out of geogig manages data etc.
                             -------------------
        begin                : 2017-11-16
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Markus Heße/Mettenmeier GmbH
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

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog, QDialogButtonBox

from geogig_package_creator_engine import GeogigPackageCreatorEngine

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'geogig_package_creator_dialog_base.ui'))


class GeogigPackageCreatorDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(GeogigPackageCreatorDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.pbSelectFile.clicked.connect(self.selectFile)
        self.pbOK.clicked.connect(self.createPackage)
        self.pbCancel.clicked.connect(self.close)
        
    def selectFile(self):
        SelectedFile = self.lineEditFileName.text()
        StartDir     = '';
        
        if SelectedFile <> '':
            SelectedDirectory = os.path.dirname(SelectedFile)
            if os.path.exists(SelectedDirectory) and os.path.isdir(SelectedDirectory):
                StartDir = SelectedDirectory
                
        self.lineEditFileName.setText(QFileDialog.getSaveFileName(self, 
                                                                  caption   = 'Select file for package',
                                                                  directory = StartDir))


    def createPackage(self):
            Engine = GeogigPackageCreatorEngine()
            Engine.progressChanged.connect(self.on_progress)
            Engine.run(self.lineEditFileName.text(), 
                       withDatabases    = self.cbDatabase.isChecked(),
                       withProject      = self.cbQgisProject.isChecked(), 
                       withConfiguration= self.cbGeogigConfig.isChecked(), 
                       withPlugins      = self.cbGeogigPlugins.isChecked())
            
            
    def on_progress(self, progressValue, progressString):
        # If a negative value is given, I leave the progress as it is.
        # Nice feature, if I only want to change the label text.
        if not (progressValue < 0):
            self.progressBar.setValue(progressValue) 

        self.progressLabel.setText(progressString)
            
            