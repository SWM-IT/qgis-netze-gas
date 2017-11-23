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
from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest, QgsDataSourceURI, QgsWKBTypes, QGis, QgsVectorLayer, QgsFeature, QgsGeometry, QgsMessageLog, QgsSpatialIndex
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from topoGeomAdd_dialog import TopologicGeometryAddDialog
# Import the topology connector class
from TopologyConnector import TopologyConnector
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
        
        # set db connector for topology tests
        self.topologyConnector = TopologyConnector()
                
        # set variables as typ array
        self.qgisLayerInformation = []
        self.postgresLayerInformation = []
        self.deletedQgisLayerInformation = []        
                
        currentLayer = self.iface.mapCanvas().currentLayer()
        if currentLayer:
            self.listenLayerChanged(currentLayer)                 
                
        # set signal for listenLayerChangged
        QObject.disconnect(self.iface.mapCanvas(), SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.listenLayerChanged)
        QObject.connect(self.iface.mapCanvas(), SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.listenLayerChanged)
                   

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
        
        
    def listenLayerChanged(self, currentLayer):
        '''
        listen signal if layer changed
        '''
        
        if not (self.nodeLayer and self.edgeLayer):
            for aLayer in QgsMapLayerRegistry.instance().mapLayers().values():
                if aLayer.name() == u'edge':
                    self.edgeLayer = aLayer
                if aLayer.name() == u'node':
                    self.nodeLayer = aLayer
                    
        # disconnect signals 
        if self.selectedLayer and self.selectedLayer.shortName() :
 
            self.selectedLayer.featureAdded.disconnect(self.featureAdded)                
            self.selectedLayer.editingStopped.disconnect(self.editingStopped)            
            self.selectedLayer.beforeCommitChanges.disconnect(self.featuresDeleted)
            #currentLayer.beforeCommitChanges.disconnect(self.featureAdded)
              
        
        if currentLayer and currentLayer.shortName():
            ''' set Signals '''
            currentLayer.featureAdded.connect(self.featureAdded)  
            currentLayer.editingStopped.connect(self.editingStopped)
            currentLayer.beforeCommitChanges.connect(self.featuresDeleted) 
            #currentLayer.beforeCommitChanges.connect(self.featureAdded) 
            
        # store new selected layer
        self.selectedLayer = currentLayer    
              
        
    def featuresDeleted(self):
        '''
        collect deleted fids for each layer
        FIXME - we can only delete features for the actual selected layer
        '''
        
        layer = self.selectedLayer 
        
        if layer.editBuffer():
            ids = layer.editBuffer().deletedFeatureIds()
            
            if len(ids) > 0:
               for feature in layer.dataProvider().getFeatures(QgsFeatureRequest().setFilterFids(ids)):
                   
                   # get systemid
                   systemId = feature['system_id'] 
                   
                   # get geom type
                   geom = feature.geometry()               
                   if geom.type() == QGis.Point:
                       geom_type = "node"
                   
                   elif geom.type() == QGis.Line:
                        geom_type = "edge"
                        
                   # store feature informations for database operations
                   self.deletedQgisLayerInformation.append({'system_id': systemId, 'layername': self.selectedLayer.name(), 'shortname': self.selectedLayer.shortName(), 'geomType': geom_type})
                  
            if len(self.deletedQgisLayerInformation) > 0:
                # delete feature informations in database
                self.topologyConnector.deleteFeatureInformations(self.deletedQgisLayerInformation)
        
                # repaint node and edge layer (refresh map)        
                self.edgeLayer.triggerRepaint()
                self.nodeLayer.triggerRepaint()   
                            
      
    def editingStopped(self):
        '''
        signal when editing is stopped 
        '''       
       
        # add geomLayers for each postgresLayer
        self.addGeomLayers()       
              
        # clear array from method featuresDeleted
        self.deletedQgisLayerInformation = []     
                       
        
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
        
        
    def featureAdded(self, fid):
        '''
        callback for Signal addedFeature
        collect my added Features for later
        '''
          
        # fetch not commited features
        if fid < 0:
            #self.qgisLayerFIDS.append(fid)
            self.qgisLayerInformation.append({'fid': fid, 'layername': self.selectedLayer.name(), 'shortname': self.selectedLayer.shortName()})
        else: 
            # commited features            
            self.postgresLayerInformation.append({'fid': fid, 'layername': self.selectedLayer.name(), 'shortname': self.selectedLayer.shortName()})
      
    
        
    def insertGeomTopoInformations(self):
        '''
        insert necessary entrys in postgres DB eg. relations, generating topogeomId etc.
        '''
        
        for properties in self.postgresLayerInformation:
            
            featureID = properties['fid'] # fid from featureLayer
                        
            # get right qgis layer for selection featureId            
            for aLayer in QgsMapLayerRegistry.instance().mapLayers().values():
                if aLayer.name() == properties['layername']:
                    featureLayer = aLayer 
            
            iterator = featureLayer.getFeatures(QgsFeatureRequest().setFilterFid(featureID))
            try:
                feature = next(iterator) 
                
                systemId = feature['system_id'] 
                self.topologyConnector.setTopoGeometryData(systemId, properties)
                
            except StopIteration:
                raise Exception( "Fehler beim setzen des TopoInformationen..Abbruch")
                
        # clear array
        self.postgresLayerInformation = []
                
        
    def addGeomLayers(self):
        '''
        set topoGeom Objects for each layer
        ''' 
        
        for i in self.postgresLayerInformation:
            
            # set default values
            i['geomLayerStartNodeFid'] = ""
            i['geomLayerEndNodeFid'] = ""
            i['geomLayerEdgeFid'] = ""
            i['geomLayerNodeFid'] = ""
            
            featureID = i['fid']  
            
            # FIX ME
            # signal commit changes only geomlayers generated for selectedLayer
            if self.selectedLayer.name() != i['layername']:
                continue 
            
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
                                                
                if geom_type == "edge":
                       
                    firstNodeGeom = a_geom[0]
                    lastNodeGeom  = a_geom[len(a_geom)-1]
                    
                    firstQgisGeomPoint = QgsGeometry.fromPoint(firstNodeGeom)
                    lastQgisGeomPoint = QgsGeometry.fromPoint(lastNodeGeom)
                    
                    firstExistingNodeId = self.checkForExistingGeomNode(firstQgisGeomPoint)
                    lastExistingNodeId = self.checkForExistingGeomNode(lastQgisGeomPoint)
                                           
                    # for firstNode - add new node                 
                    if firstExistingNodeId is False:                        
                        
                        firstGeneratedNodeId = self.addNodeFeature(firstQgisGeomPoint)                        
                        i['geomLayerStartNodeFid'] = firstGeneratedNodeId                      
                        
                    else: # get existing firstNode
                    
                        firstGeneratedNodeId = firstExistingNodeId
                        i['geomLayerStartNodeFid'] = firstExistingNodeId
                    
                    # for lastNode - add new node   
                    if lastExistingNodeId is False:
                        
                        lastGeneratedNodeId = self.addNodeFeature(lastQgisGeomPoint)                         
                        i['geomLayerEndNodeFid'] = lastGeneratedNodeId 
                    
                    else: # get existing lastNode
                    
                        lastGeneratedNodeId = lastExistingNodeId
                        i['geomLayerEndNodeFid'] = lastExistingNodeId  
                    
                    # make a new edge geom with first and last node from line                     
                    newEdgePoly = []                    
                    newEdgePoly.append(firstNodeGeom)
                    newEdgePoly.append(lastNodeGeom)
                    edgeGeom = QgsGeometry.fromPolyline(newEdgePoly)
                                       
                    # set edge in qgis
                    generatedEdgeId = self.addEdgeFeature(edgeGeom, firstGeneratedNodeId, lastGeneratedNodeId)                    
                    
                    i['geomLayerEdgeFid'] = generatedEdgeId 
                    i['geomType'] = geom_type 
                    
                elif geom_type == "node":
            
                    # check if a node already exists on geom position              
                    existingNodeId = self.checkForExistingGeomNode(geom) 
                    
                    i['geomType'] = geom_type 
                     
                    # add new geomNode               
                    if existingNodeId is False:
                        
                        qgis_geom = QgsGeometry.fromPoint(a_geom)
                        generatedNodeId = self.addNodeFeature(qgis_geom) 
                        i['geomLayerNodeFid'] = generatedNodeId                                             
                        
                    elif existingNodeId:   
                        
                        # get NodeId from existing Node on position                        
                        i['geomLayerNodeFid'] = existingNodeId
                
            except StopIteration:
                raise Exception( "Fehler beim setzen des Geom Layers / Node Layers..Abbruch")
            
            
        # insert Topo Informations in postgres DB
        self.insertGeomTopoInformations()
        
        
    def addNodeFeature(self, qgis_geom):
        '''
        add node(s) for each added layer
        '''
                
        # set Feature geomLayer
        feat = QgsFeature(self.nodeLayer.pendingFields())
        feat.setGeometry(qgis_geom)
        (result, outFeats) = self.nodeLayer.dataProvider().addFeatures([feat]) 
    
        # commit to stop editing the layer
        self.nodeLayer.commitChanges()
            
        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        self.nodeLayer.updateExtents()
        
        # add layer to the legend
        QgsMapLayerRegistry.instance().addMapLayer(self.nodeLayer)
        
        if result == False:
            
            raise Exception( "Fehler beim anlegen des Features für den NODE Layer..Abbruch")
        
                          
        return outFeats[0].id()
    
          
    def addEdgeFeature(self, edgeGeom, firstGeneratedNodeId, lastGeneratedNodeId):
        '''
        add edge for added layer
        '''
        
        # FIX ME
        # get dummy edge_id from DB while without an existing edge_id
        # we cannot commit a edge        
        an_edge_id = self.topologyConnector.getAEdgeId()
        
        if getAEdgeId is False:
            
            return False
        
        else:         
            edge_id = an_edge_id+1 # new edgeId for entry
            ########
        
            # set Feature geomLayer
            feat = QgsFeature(self.edgeLayer.pendingFields())
            feat = QgsFeature()
            feat.setGeometry(edgeGeom)
        
            # set attributes for feature
            feat.setAttributes([edge_id, firstGeneratedNodeId, lastGeneratedNodeId, an_edge_id, an_edge_id, an_edge_id, an_edge_id, 0 , 0])
                           
            (result, outFeats) = self.edgeLayer.dataProvider().addFeatures([feat]) 
    
            # commit to stop editing the layer
            self.edgeLayer.commitChanges()
            
            # update layer's extent when new features have been added
            # because change of extent in provider is not propagated to the layer
            self.edgeLayer.updateExtents()
        
            # add layer to the legend
            QgsMapLayerRegistry.instance().addMapLayer(self.edgeLayer)
        
            if result == False:
            
                raise Exception("Fehler beim anlegen des Features für den EDGE Layer..Abbruch")
                          
            return outFeats[0].id()
        
    
    def checkForExistingGeomNode(self, geom):
        '''
        check if geometry (bounding_box) from the featureLayer (e.g. Hausanschluss) within a node        
        '''
        
        featsPnt = self.nodeLayer.getFeatures(QgsFeatureRequest().setFilterRect(geom.boundingBox()))
        for featPnt in featsPnt:
             #iterate preselected point features and perform exact check with current point
            if featPnt.geometry().within(geom):
                                
                # give back fid from node                
                print("Node gefunden: " + str(featPnt[0]))
                return featPnt[0]
            
        return False
        
            
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


    '''
        QgsMessageLog.logMessage( 'adjust coordinates not successfull', 'TopoPluginAdd', 2)
    
        #feat.setAttributes(['node_id', nextval('gas_topo.node_node_id_seq'::regclass)])
        #feat.setAttributes(['containing_face', 111111111]) # vl. Feature ID vom aktiv Layer reinschreiben                
        #feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(4464012.2,5335163.8))) 
        
         funkioniert so nicht - warum nicht ???
        feat.setAttributes(['edge_id', edge_id]) # we have to set, i don't know why ????
        feat.setAttributes(['start_node', firstGeneratedNodeId]) 
        feat.setAttributes(['end_node', lastGeneratedNodeId]) 
        feat.setAttributes(['next_left_node', an_edge_id]) 
        feat.setAttributes(['abs_next_left_node', an_edge_id]) 
        feat.setAttributes(['next_right_node', an_edge_id])   
        feat.setAttributes(['abs_next_right_node', an_edge_id])
        feat.setAttributes(['left_face', 0]) 
        feat.setAttributes(['right_face', 0])
        
        
        # intersections     
        spi = QgsSpatialIndex( self.nodeLayer.getFeatures() ) 
        intersectIds = spi.intersects( geom.boundingBox().buffer(1) ) 
    '''
   