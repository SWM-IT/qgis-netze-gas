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
            
            
    def setTopoGeometryData(self, systemId, TableName, geomLayerProperties):
        '''
        returns the geometry of a topo node with the given nodeId
        '''
        
        '''
        print("IN setTopoGeometryData")
        print(systemId)
        
        print("Table Name")
        print(TableName)
        '''
        
        if systemId:
                                       
            # get Layer properties...topoGeomId etc.
            LayerProperties = self.getNextTopoGeomIdAndProperties(TableName)           
              
            # update layer table tuple  
            self.updateLayerTuple(LayerProperties, systemId, TableName) 
                        
            # get elementID from node or edge table    
            self.createRelationTableEntry(geomLayerProperties, LayerProperties)         
               
            
            
    def createRelationTableEntry(self, geomLayerProperties, LayerProperties):
        '''
        insert relation entry between layer table and node or edge table
        '''
        
        #print("IN createRelationTableEntry")
        
        schema = "gas_topo" 
        geomTableName = "relation"         
        
        topoGeomId = LayerProperties[0]
        layer_id = LayerProperties[1]
        element_type = LayerProperties[2]
        #topology_id = properties[3]
    
                                    
        fid = geomLayerProperties['fid'] # is node_id or edge_id
        
        #geomType = geomLayerProperties[2]
        #geomTableName = geomLayerProperties[3]   
        
        conn = self.db_connection(None, None, None, None)
        if conn:
            
            cur = conn.cursor() 
            
            '''
            print("---------")
            print(topoGeomId)
            print(layer_id)
            print(fid)
            print(element_type)
            '''
            #cur.execute("INSERT INTO " + schema + "." + str(geomTableName) + " (topogeo_id, layer_id, element_id, element_type) VALUES ('" + str(topology_id) + "', '" + str(layer_id) + "', '" + str(fid) + "', '" + str(element_type) + "' ) ")
                      
            cur.execute("INSERT INTO gas_topo.relation VALUES ('" + str(topoGeomId) + "', '" + str(layer_id) + "', '" + str(fid) + "', '" + str(element_type) + "' ) ")
            conn.commit()
            
            self.db_connection_close() 
                
            print("INSERT RELATION ENTRY !!")
    
    
    def updateLayerTuple(self, properties, systemId, TableName):
        '''
        update Tuples for added layers column g
        '''
                
        schema = "ga"  
                                    
        topoGeomId = properties[0]
        layer_id = properties[1]
        element_type = properties[2]
        topology_id = properties[3]
        
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
            
            self.db_connection_close() 
            
            if len(row) == 0:
                print("Fehler DB: TOPOGEOD ID wurde nicht generiert")
                return False
            else:
                return row  
            
                