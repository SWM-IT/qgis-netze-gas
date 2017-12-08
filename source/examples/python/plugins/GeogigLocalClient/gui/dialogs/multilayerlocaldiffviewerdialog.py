# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MultiLayerLocalDiffViewerDialog
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

from qgis.PyQt.QtWidgets import (QTreeWidgetItem)
from qgis.PyQt.QtGui import QIcon

from geogig.gui.dialogs.localdiffviewerdialog import (LocalDiffViewerDialog, 
                                                      layerIcon, 
                                                      featureIcon, 
                                                      addedIcon, 
                                                      removedIcon, 
                                                      modifiedIcon)
from geogig.geogigwebapi.diff import LOCAL_FEATURE_ADDED, LOCAL_FEATURE_MODIFIED, LOCAL_FEATURE_REMOVED


class MultiLayerLocalDiffViewerDialog(LocalDiffViewerDialog):
    
    def __init__(self, parent, layers):
        self.layers = layers
        super(MultiLayerLocalDiffViewerDialog, self).__init__(parent, layers[0])
        
    def computeDiffs(self):
        # FIXME: Mostly copied from LocalDiffViewerDialog. But I need to iterate over all layers here
        self.featuresTree.clear()
        
        self.changes = {}
        for layer in self.layers:
            self.changes.update(self.localChanges(layer))
            layerItem = QTreeWidgetItem()
            layerItem.setText(0, layer.name().encode('utf-8'))
            layerItem.setIcon(0, layerIcon)
            self.featuresTree.addTopLevelItem(layerItem)
            addedItem = QTreeWidgetItem()
            addedItem.setText(0, "Added")
            addedItem.setIcon(0, addedIcon)
            removedItem = QTreeWidgetItem()
            removedItem.setText(0, "Removed")
            removedItem.setIcon(0, removedIcon)
            modifiedItem = QTreeWidgetItem()
            modifiedItem.setText(0, "Modified")
            modifiedItem.setIcon(0, modifiedIcon)
            layerSubItems = {LOCAL_FEATURE_ADDED: addedItem,
                             LOCAL_FEATURE_REMOVED: removedItem,
                             LOCAL_FEATURE_MODIFIED: modifiedItem}

            for c in list(self.changes.values()):
                item = QTreeWidgetItem()
                item.setText(0, c.fid)
                item.setIcon(0, featureIcon)
                layerSubItems[c.changetype].addChild(item)

            for i in [LOCAL_FEATURE_ADDED, LOCAL_FEATURE_REMOVED, LOCAL_FEATURE_MODIFIED]:
                layerItem.addChild(layerSubItems[i])
                layerSubItems[i].setText(0, "%s [%i features]" % (layerSubItems[i].text(0), layerSubItems[i].childCount()))

            self.attributesTable.clear()
            self.attributesTable.verticalHeader().hide()
            self.attributesTable.horizontalHeader().hide()

        self.featuresTree.expandAll()
        
 