'''
Created on 09.11.2017

@author: thomasst
'''
import psycopg2
from PyQt4.QtGui import QMessageBox
from platform import node
from __builtin__ import str
from TopoLine import TopoLine


class TopologyConnector():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.connection = None
        
    def db_connection(self, host, dbname, user, password):
        '''
        returns a database connection with given parameter
        '''
        toolname = "TopologyConnector"
        
        if not self.connection:
        
            if not host:
                host = "localhost"
            if not dbname:
                dbname = "nisconnect_integration"
            if not user:
                user = "postgres"
            if not password:
                password = "postgres"
            
            try:
                conn = psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='" + host + "' password='" + password + "'")
                self.connection = conn
                return conn
            except:
                # show error
                QMessageBox.critical(None, toolname, "There was an error connecting to the database.")
        else:
            return self.connection
            
    def db_connection_close(self):
        '''
        close the connection to the database
        '''
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def setLayerInfo(self, aLayerDbInfo):
        '''
        store DB information of current selected Layer
        '''
        self.layerDbInfo = aLayerDbInfo
            
            
    def setTopoGeometryData(self, systemId, properties):
        '''
        returns the geometry of a topo node with the given nodeId
        '''
        
        TableName = properties['shortname']          
        
        if systemId:
                                       
            # get Layer properties...topoGeomId etc.
            layerProperties = self.getNextTopoGeomIdAndProperties(TableName)           
              
            # update layer table tuple  
            self.updateLayerTuple(layerProperties, systemId, TableName) 
                        
            # get elementID from node or edge table    
            self.createRelationTableEntry(layerProperties, properties) 
            
            
    def createRelationTableEntry(self, layerProperties, properties):
        '''
        insert relation entry between layer table and node or edge table
        '''
        
        #print("IN createRelationTableEntry")
        
        schema = "gas_topo" 
        TableName = "relation"         
        
        # get properties from actual postgres layer
        topoGeomId = layerProperties[0]
        layer_id = layerProperties[1]
        element_type = layerProperties[2] 
                
        
        geomLayerNodeFid = properties['geomLayerNodeFid'] # fid from geomLayer            
        geomLayerEdgeFid = properties['geomLayerEdgeFid']
        geomType = properties['geomType'] 
        geomLayerStartNodeFid = properties['geomLayerStartNodeFid']
        geomLayerEndNodeFid= properties['geomLayerEndNodeFid']
          
        '''
        print("------")
        print("TOPGEOMID")
        print(topoGeomId)
        print("LAYER ID ")
        print(layer_id)
        print("ELEMENT TYPE")
        print(element_type)
        #print("geomLayerFid")
        #print(geomLayerFid)
        '''
        
        conn = self.db_connection(None, None, None, None)
        if conn:
            
            cur = conn.cursor() 
            
            # relations for edges
            if geomType == "edge":
                
                cur.execute("INSERT INTO " + schema + "." + str(TableName) + " VALUES ('" + str(topoGeomId) + "', '" + str(layer_id) + "', '" + str(geomLayerEdgeFid) + "', '" + str(element_type) + "' ) ")
                 
                print("INSERT RELATION EDGE ENTRY !!")
                
                '''
                update start_node / end_node on table edge_data for edge_id
                ''' 
                edge_data = "edge_data"
                cur.execute("UPDATE " + schema + "." + str(edge_data) + " SET start_node = '" + str(geomLayerStartNodeFid) + "', end_node = '" + str(geomLayerEndNodeFid) + "' WHERE edge_id= '" + str(geomLayerEdgeFid) + "' ")  
                
                print("Aktualisiere Eintraege in edge_data Eintrag edge_id")
                #print(geomLayerEdgeFid)
                
            # relations for nodes     
            if geomType == "node":
            
                cur.execute("INSERT INTO " + schema + "." + str(TableName) + " VALUES ('" + str(topoGeomId) + "', '" + str(layer_id) + "', '" + str(geomLayerNodeFid) + "', '" + str(element_type) + "' ) ")
                
                print("INSERT RELATION NODE ENTRY !!")
                #print(geomLayerNodeFid)
            
            conn.commit()
            
            #self.db_connection_close() 
    
    
    def updateLayerTuple(self, properties, systemId, TableName):
        '''
        update Tuples for added layers column g
        '''
                
        schema = "ga"  
                                     
        topoGeomId = properties[0]
        layer_id = properties[1]
        element_type = properties[2]
        topology_id = properties[3]
        
        #print("NEUE TOPOGEOID")
        #print(topoGeomId)
        
        conn = self.db_connection(None, None, None, None)
        if conn:
                    
            cur = conn.cursor() 
            cur.execute("UPDATE " + schema + "." + str(TableName) + " SET g = ('" + str(topology_id) + "', '" + str(layer_id) + "', '" + str(topoGeomId) + "', '" + str(element_type) + "') WHERE system_id= '" + str(systemId) + "' ")  
            
            conn.commit()
            
            self.db_connection_close() 
                
            #print("UPDATE TUPLE !!")
            
            
    def getNextTopoGeomIdAndProperties(self, TableName):
        '''
        returns the next topoGeom_Id and properties eg layer_id, feature_type etc.
        '''
        
        conn = self.db_connection(None, None, None, None)
        if conn:  
            
            cur = conn.cursor()
            cur.execute("""SELECT max(r.topogeo_id) +1 AS topogeo_id, l.layer_id AS layer_id, l.feature_type, l.topology_id AS element_type FROM topology.layer l, gas_topo.relation r WHERE l.layer_id = r.layer_id AND l.table_name='""" +  TableName  + """' GROUP BY l.layer_id, l.feature_type, l.topology_id LIMIT 1 """) 
           
            row = cur.fetchone()
            
            #self.db_connection_close() 
            
            if len(row) == 0:
                print("Fehler DB: TOPOGEOD ID wurde nicht generiert")
                return False
            else:
                return row 
            
           
    def getAEdgeId(self):      
        
        schema = "gas_topo"
        geomTableName = "edge_data"        
        
        conn = self.db_connection(None, None, None, None)
        if conn:  
            
            cur = conn.cursor()  
                        
            # get next edge_id 
            cur.execute("""SELECT max(edge_id) FROM """ + schema + """.""" + str(geomTableName) + """ LIMIT 1""") 
            row = cur.fetchone()
            
            if len(row) == 0:
                print("Fehler DB: TOPOGEOD ID wurde nicht generiert")
                return False
            else:
                return row[0] 
            
    