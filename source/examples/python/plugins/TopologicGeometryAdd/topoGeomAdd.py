# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TopologicGeometryAdd
                                 A QGIS plugin
 add new objects with topo geoms
                              -------------------
        begin                : 2017-10-25
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Thomas Starke
        email                : thomas.starke@mettenmeier.de
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QObject, SIGNAL, pyqtSlot
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest, QgsDataSourceURI, QgsWKBTypes, QGis, QgsVectorLayer, QgsFeature, QgsGeometry, QgsMessageLog
#from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from topoGeomAdd_dialog import TopologicGeometryAddDialog
# Import the topology connector class
from TopologyConnector import TopologyConnector
from LayerDbInfo import LayerDbInfo
import os.path
from qgis.utils import iface
from PyQt4.Qt import QColor
# time to check performance issues
import time

import os



class TopologicGeometryAdd:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """        
        
        # Save reference to the QGIS interface
        self.iface = iface
        
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'TopologicGeometryEdit_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Topologic Geometry Add')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'TopologicGeometryAdd')
        self.toolbar.setObjectName(u'TopologicGeometryAdd')
        # declare slot variables
        self.selectedLayer = None
        self.nodeLayer = None
        self.edgeLayer = None
        self.layerInfo = None # holds information of current selected layer
        
        # set db connector for topology tests
        self.topologyConnector = TopologyConnector()
        
        self.commitedChanges = False # store information if geomLayers are set  
        self.lastModifiedLayer = False    
        
        self.qgisLayerInformation = []
        self.postgresLayerInformation = []
        
        # start method for listening signals
        #self.listenSignals(None)
                
        currentLayer = self.iface.mapCanvas().currentLayer()
        if currentLayer:
            self.listenLayerChanged(currentLayer)                 
                
        # set signal for layerchanged
        QObject.connect(self.iface.mapCanvas(), SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.listenLayerChanged)
        
        
        print("RELOAD PLUGIN")


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('TopologicGeometryEdit', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = TopologicGeometryAddDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action
    

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/TopologicGeometryEdit/icon.png'
        
        self.add_action(
            icon_path,
            text=self.tr(u'Add Topologic Geometry'),
            callback=self.checkIfLayerSelected,
            parent=self.iface.mainWindow())
        
                
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Topologic Geometry Add'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar     
              
    '''
    def listenSignals(self, layer):
       
        #print("IN LISTEN SIGNALS")
        
        # check if already a layer is selected on Plugin Load (probably only during testing)         
        if self.selectedLayer:            
            
            #print("Überschreibe Layer")
            self.selectedLayer = layer              
            
        else:
            #print("Setze Layer neu")
            self.selectedLayer = self.iface.mapCanvas().currentLayer()
            
        
        if self.selectedLayer:  
            
            self.selectedLayer.featureAdded.connect(self.listenLayer)            
            self.selectedLayer.beforeCommitChanges.connect(self.commitChanges) 
    '''  
        
        
    def listenLayerChanged(self, currentLayer):
        '''
        listen signal if layer changed
        '''
        
        #print("-------------------------")
        print("IN LISTEN LAYER CHANGED")
        
        if not (self.nodeLayer and self.edgeLayer):
            for aLayer in QgsMapLayerRegistry.instance().mapLayers().values():
                if aLayer.name() == u'edge':
                    self.edgeLayer = aLayer
                if aLayer.name() == u'node':
                    self.nodeLayer = aLayer
        
        
        # evtl. muss man auf die beendete Bearbeitung eines Layer reagieren
        '''
        if self.lastModifiedLayer:
            
            if self.lastModifiedLayer.isModified() == False:
            
                self.commitedChanges = False 
            
                #print("letzter Modifizierter Layer")
                #print(self.lastModifiedLayer.name())
        '''
        
        #print("--------")
        if currentLayer and currentLayer.shortName():
            
            #print("DER CURRENT LAYER")
            #print(currentLayer.name())
            
            ''' set Signals '''
            currentLayer.featureAdded.connect(self.listenLayer)            
            currentLayer.beforeCommitChanges.connect(self.commitChanges) 
            
            currentLayer.editingStopped.connect(self.editingStopped)
            currentLayer.featuresDeleted.connect(self.featuresDeleted)
            
        
        # disconnect signals 
        if self.selectedLayer and self.selectedLayer.shortName() :                
            '''disconnect signals'''  
            
            #print("DER SELECTED LAYER")
            #print(self.selectedLayer.name()) 
                  
            self.selectedLayer.featureAdded.disconnect()    
            self.selectedLayer.beforeCommitChanges.disconnect()    
            
            self.selectedLayer.editingStopped.disconnect()
            self.selectedLayer.featuresDeleted.disconnect() 
            
        # store new selected layer
        self.selectedLayer = currentLayer 
          
        # set new signal on selected layer     
        #self.listenSignals(layer)
        
    def featuresDeleted(self,fid):
        
        print("IN featuresDeleted sIGANL ")
        #print("FID")
        #print(fid)
        
        
    def editingStopped(self):
        
        print("IN editingStopped sIGANL ")
        
        print(len(self.postgresLayerInformation))
        for i in self.postgresLayerInformation:
            print(i['fid'])
        
        #self.commitedChanges = False 
                       
        
    def checkIfLayerSelected(self):   
        '''
        check if a layer is selected
        '''        
        
        toolname = "TopologicAdd"

        # check that a layer is selected        
        layer = self.iface.mapCanvas().currentLayer()
        if not layer:
          QMessageBox.information(None, toolname, "A layer must be set active")
          return
        
        # check that the selected layer is a postgis one
        if layer.providerType() != 'postgres':
          QMessageBox.information(None, toolname, "A PostGIS layer must be selected")
          return
      
        uri = QgsDataSourceURI( layer.source() )

        # get the layer schema
        schema = str(uri.schema())
        if not schema:
          QMessageBox.information(None, toolname, "Selected layer must be a table, not a view\n"
            "(no schema set in datasource " + str(uri.uri()) + ")")
          return
      
        # get the layer table
        table = str(uri.table())
        if not table:
          QMessageBox.information(None, toolname, "Selected layer must be a table, not a view\n"
            "(no table set in datasource)")
          return
    
        
        
    def listenLayer(self, fid):
        '''
        callback for Signal addedFeature
        '''
                    
        # fetch not commited features
        if fid < 0:
            #self.qgisLayerFIDS.append(fid)
            self.qgisLayerInformation.append({'fid': fid, 'layername': self.selectedLayer.name(), 'shortname': self.selectedLayer.shortName()})
        else: 
            # commited features            
            self.postgresLayerInformation.append({'fid': fid, 'layername': self.selectedLayer.name(), 'shortname': self.selectedLayer.shortName()})
        
        
        # after my geom Layers commited
        if self.commitedChanges == True: #and len(self.postgresLayerInformation > 0):
            
            self.updateInsertGeomTopoInformations()     
            
            # clear array 
            self.postgresLayerInformation = []
                   
        
    def updateInsertGeomTopoInformations(self):
        '''
        insert necessary entrys in postgres DB eg. relations, generating topogeomId etc.
        '''
                
        ##print("IN updateInsertFeatureInformations")
        
        for i in self.postgresLayerInformation:
            
            shortname = i['shortname']      
            featureID = i['fid']  
            
            # set Flag
            geomLayerProperties = False
                        
            # get right qgis layer for selection of featureId            
            for aLayer in QgsMapLayerRegistry.instance().mapLayers().values():
                if aLayer.name() == i['layername']:
                    featureLayer = aLayer 
            
            iterator = featureLayer.getFeatures(QgsFeatureRequest().setFilterFid(featureID))
            try:
                feature = next(iterator) 
                
                systemId = feature['system_id']               
                geom = feature.geometry()
                
                if geom.type() == QGis.Point:
                    a_geom = geom.asPoint()
                    
                elif geom.type() == QGis.Line:
                    a_geom = geom.asPolyline()       
                
                '''
                FIX ME, i'am not sure what is the best solution, 
                but i have no mapping between hausanschluss and node  
                i search for the equal geom from each layer              
                '''
                # get right geomLayer - check equal geometry
                for g in self.geomLayerInformation:
                    print(g['geom'])
                    if g['geom'] == a_geom:
                        geomLayerProperties = g 
                        
                if geomLayerProperties == False:
                    print("keinen passenden Geom Layer gefunden")
                    return 
                
                # set topo geom data entrys on tables
                self.topologyConnector.setTopoGeometryData(systemId, shortname, geomLayerProperties)  
                
                # store my last modifiedLayer                
                self.lastModifiedLayer = featureLayer
                                 
                
            except StopIteration:
                print("Fehler")
                
                
        
    def commitChanges(self):
        '''
        fetch signal for commit Changes
        '''
        
        self.addGeomLayers()
        
        
    def addGeomLayers(self):
        '''
        set geomLayers for each layer
        '''
    
        #print("in addGeomLayers")   
        
        self.geomLayerInformation = []
    
        # gehe über die FIDS des aktiven Layer, später für alle Layer machen       
        for i in self.qgisLayerInformation:   
            
            # FIX ME
            # signal commit changes only geomlayers generated for selectedLayer
            if self.selectedLayer.name() != i['layername']:
                continue 
            
            featureID = i['fid']             
            
            # get right qgis layer            
            for aLayer in QgsMapLayerRegistry.instance().mapLayers().values():
                if aLayer.name() == i['layername']:
                    featureLayer = aLayer 
            
            iterator = featureLayer.getFeatures(QgsFeatureRequest().setFilterFid(featureID))
            try:                
                feature = next(iterator)
                            
                geom = feature.geometry()
                # show some information about the feature
                if geom.type() == QGis.Point:
                    a_geom = geom.asPoint()
                    # set geomLayer
                    geom_type = "node"
                    self.geomLayer = self.nodeLayer
                    #print "Point: " + str(a_geom)
                elif geom.type() == QGis.Line:
                    a_geom = geom.asPolyline()
                    # set geomLayer
                    geom_type = "edge"
                    self.geomLayer = self.edgeLayer
                    #print "Line: %d points" % len(a_geom)
                elif geom.type() == QGis.Polygon:
                    a_geom = geom.asPolygon()
                    numPts = 0
                    for ring in x:
                        numPts += len(ring)
                    #print "Polygon: %d rings with %d points" % (len(a_geom), numPts)
                else:
                    print "Unknown" 
            
                # set Feature for geomLayer
                feat = QgsFeature(self.geomLayer.pendingFields())
                #feat.setAttributes(['node_id', nextval('gas_topo.node_node_id_seq'::regclass)])
                #feat.setAttributes(['containing_face', 111111111]) # vl. Feature ID vom aktiv Layer reinschreiben                
                #feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(4464012.2,5335163.8)))
            
                feat.setGeometry(QgsGeometry.fromPoint(a_geom))
                (result, outFeats) = self.geomLayer.dataProvider().addFeatures([feat])
            
                # store fid from geom layer
                self.geomFid = outFeats[0].id()
                
                # store geom layer information
                self.geomLayerInformation.append({'fid': self.geomFid, 'geom': a_geom, 'geom_type': geom_type, 'layername': self.geomLayer.name()})
        
                # commit to stop editing the layer
                self.geomLayer.commitChanges()
            
                # update layer's extent when new features have been added
                # because change of extent in provider is not propagated to the layer
                self.geomLayer.updateExtents()
        
                # add layer to the legend
                QgsMapLayerRegistry.instance().addMapLayer(self.geomLayer)
                
                '''                  
                if result == True:
                    print("GEOM LAYER Gesetzt")  
                '''    
            
            except StopIteration:
                print("FEHLER beim setzen des Geom Layer")
                
            # set flag
            self.commitedChanges = True

            
    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

   