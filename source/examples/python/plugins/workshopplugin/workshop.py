import os.path
from qgis.core import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import resources
from simulation_dlg import simulationDialog
import simulation_dlg
from ftplib import print_line
#from processing.core.Processing import Processing
#Processing.initialize()
#from processing.tools import *

class Workshop:

	def __init__(self,iface):
		self.iface = iface
	
	def initGui(self):
		icon_path = ':/plugins/workshopplugin/icon1.png'
		self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())
			
		self.action = QAction(QIcon(":/plugins/workshopplugin/icon1.png"),"Gas Simulation",self.iface.mainWindow())
		
		QObject.connect(self.action, SIGNAL("activated()"),self.run)
		
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToMenu("Gas Simulation",self.action)
		
	def tr(self, message):
    	 return QCoreApplication.translate('workshop', message)
		
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
		self.dlg = simulationDialog()
		
	
	def unload(self):
		self.iface.removePluginMenu('&Gas Simulation', self.action)
		self.iface.removeToolBarIcon(self.action)
		
	def run(self):
	   	
	   	#Get the selected layer
		layer = self.iface.mapCanvas().currentLayer()
		nodes = "";
		
		#Node layer needs to be selected first
		if not layer or not (layer.name() == 'node') :
			QMessageBox.information(None,"Simulation","Select the nodelayer")
			return
		
		#Get all the selected nodes
		selected = layer.selectedFeatures()
		
		if not selected:
			QMessageBox.information(None,"Simulation","Select a starting node")
			return
			
		if selected:
			idx = layer.fieldNameIndex('node_id')
			print("Selected")
		 	for node in selected:
		 		nodes = nodes + str(node.attributes()[idx]) + ",";
		 
		# Delete the last node (its broken/empty)
		nodes = nodes[:-1];
		print nodes;
		 	
		#DataBaseInformation
		#Edit this for the installation
		db = QSqlDatabase('QPSQL')
		if db.isValid():
   			db.setHostName('localhost')
    	 	db.setDatabaseName('nisconnect_integration')
  	    	db.setUserName('postgres')
      	 	db.setPassword('postgres')
      	 	db.setPort(5432)
      	 	
  	 	#Fill the input fields with database information	
  	 	if db.open():
  	 		# Add all possible tables from the topology
  	 		#query = db.exec_("SELECT DISTINCT table_name FROM information_schema.columns WHERE table_schema = 'gas_test' AND table_name <> 'node' AND table_name <> 'relation' AND table_name <> 'face' AND table_name <> 'edge_data' AND table_name <> 'edge'")
  	 		self.dlg.comboBox.clear()
  	 		#while query.next():
  	 		#	record = query.record()
  	 		#	self.dlg.comboBox.addItem(record.value(0))
  	 			
  	 		self.dlg.comboBox.addItem("g_absperrarmatur")		
  	 		# Add all possible fields from the table (schieber)
  	 		#query = db.exec_("SELECT column_name FROM information_schema.columns WHERE table_schema = 'gas_test' AND table_name = 'absperrarmatur'")
  	 		self.dlg.comboBox_2.clear()
  	 		#while query.next():
  	 		#	record = query.record()
  	 		#	self.dlg.comboBox_2.addItem(record.value(0))
  	 		self.dlg.comboBox_2.addItem("armaturenstellung")	
  	 		# Add all possible criteriums from the field (schieber)
  	 		#query = db.exec_("SELECT DISTINCT armaturenstellung FROM gas_test.absperrarmatur")
  	 		self.dlg.comboBox_3.clear()
  	 		#while query.next():
  	 		#	record = query.record()
  	 		#	self.dlg.comboBox_3.addItem(record.value(0))
  	 		self.dlg.comboBox_3.addItem("geschlossen")
  	 		#query = db.exec_("SELECT DISTINCT schema_name FROM information_schema.schemata where schema_name !~ '(pg)'")
  	 		self.dlg.select_topology.clear()
  	 		#while query.next():
  	 		#	record = query.record()
  	 		#	self.dlg.select_topology.addItem(record.value(0))
  	 		#self.dlg.select_topology.addItem("gas_test")
  	 		self.dlg.select_topology.addItem("gas_topo")
  	 			
 		self.dlg.show()
	 	result = self.dlg.exec_()
		
		#Start the simulation
		if result:
			
			layer = self.iface.mapCanvas().currentLayer()
			if not (layer.name() == "edge") :
				QMessageBox.information(None,"Simulation","Select the edge layer")
				return
		
			#Get the information e
			scheme = "ga" # FIXME: Hardcoded Scheme!! Should be retrieved from the layer table
			table = self.dlg.comboBox.currentText()
			attribute = self.dlg.comboBox_2.currentText()
			criterium = self.dlg.comboBox_3.currentText()
			topology = self.dlg.select_topology.currentText()
			
			print "Simulation start"
			result=[]
			selection=[]
			if db.open():
	   			query = db.exec_(" select * from topology.simulate(\'" + nodes + "\',\'" + topology + "\',\'" + scheme + "\',\'" + table + "\',\'" + attribute + "\',\'" + criterium + "\')")
	   			while query.next():
	   				record = query.record()	   	
	   				result.append(record.value(0))			
	   			print "Simulation end"
	   			
	   			layer = self.iface.mapCanvas().currentLayer()
	   			idx2 = layer.fieldNameIndex('edge_id')
	   			
	   			
	   			
	   			
	   			
	   			for resulted in result:
	   				request = QgsFeatureRequest().setFilterExpression(u'"edge_id" = ' + str(resulted))
	   				request.setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes(['id'], layer.fields())
	   				for feature in layer.getFeatures(request):
	   					selection.append(feature.id())
	   				
	   					
	   		#Make a selection			
	   		layer.setSelectedFeatures(selection)
	   		print "Selection end"
	   		
	   		## Create Temporary Layer ##
			temp = QgsVectorLayer("LineString?crs=epsg:31468",self.dlg.layer_name.text(), "memory")
			temp_data = temp.dataProvider()
			attr = layer.dataProvider().fields().toList()
			temp_data.addAttributes(attr)
			temp.updateFields()
			temp_data.addFeatures(layer.selectedFeatures())
			QgsMapLayerRegistry.instance().addMapLayer(temp)
	   		print "Creation end"
	   		
	   	

			