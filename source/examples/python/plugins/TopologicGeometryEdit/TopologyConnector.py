'''
Created on 15.09.2017

@author: fischerh
'''
import psycopg2
from PyQt4.QtGui import QMessageBox
from platform import node
from __builtin__ import str

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
    
    def all_edges_for_node(self, nodeId):
        '''
        returns all connected edges to a node
        '''
        if nodeId:
            # get db connection
            conn = self.db_connection(None, None, None, None)
            if conn:
                # get edge entries from relations table
                cur = conn.cursor()
                tableName = "gas_topo.edge_data"
                cur.execute("""SELECT e.edge_id, e.geom from """ + tableName + """ e WHERE e.start_node = """ + str(nodeId) + """ OR e.end_node = """ + str(nodeId))
                
                rows = cur.fetchall()
                
                edgeIds = []
                
                for row in rows:
                    edgeIds.append({'edgeId': row[0], 'edgeGeom': row[1]})
                    
                # close connection
                #self.db_connection_close()
                
                return edgeIds
            
            
        
    def all_nodes_for_edge(self, edgeId):
        '''
        returns all connected nodes to an edge
        '''
        
    def get_nodeid_for_point(self, aPointObject):
        '''
        returns the id of the topology node related to the given point object
        '''
        aPointId = aPointObject.attribute("system_id")
        if self.layerDbInfo and aPointId:
            # get db connection
            conn = self.db_connection(None, None, None, None)
            if conn:
                nodeId = None
                # get db entry for point object
                # exemplary house connection table - should be retrieved from selected layer
                cur = conn.cursor()
                #haTableName = self.layerDbInfo.getFullTableName() # "ga.g_hausanschluss"
                haTableName = "ga." + self.layerDbInfo.getTable()
                reTableName = "gas_topo.relation"
                
                cur.execute("""SELECT f.element_id from """ + haTableName + """ e, """ + reTableName + """ f WHERE e.system_id = """ + str(aPointId) + """ AND f.topogeo_id = id(e.g) AND f.element_type = 1""")
                
                rows = cur.fetchall()
                
                # should be only one
                if len(rows) > 0:
                    nodeId = rows[0][0]
                    
                # close connection
                #self.db_connection_close()
                
                return nodeId
        
    def get_edgeid_for_line(self, aLineObject):
        '''
        returns the id of the topology edge related to the given line object
        '''
        
    def get_point_for_nodeid(self, nodeId):
        '''
        returns the point object related to the given node id
        '''
        
    def get_lines_for_edgeids(self, edgeIds):
        '''
        returns the line objects related to the given edge ids
        '''
        if edgeIds:
            conn = self.db_connection(None, None, None, None)
            if conn:
                lineId = None
                cur = conn.cursor()
                reTableName = "gas_topo.relation"
                alTableName = "ga.g_anschlussltg_abschnitt"
                topoTableName = "topology.layer"
                #cur.execute("""SELECT e.topogeo_id from """ + reTableName + """ e WHERE e.element_id = """ + str(edgeId) + """ AND e.element_type = 2""")
                cur.execute("""SELECT f.system_id, e.element_id from """ + reTableName + """ e, """ + alTableName + """ f, """ + topoTableName + """ h WHERE e.element_id in (""" + ','.join(map(str, edgeIds)) + """) AND e.element_type = h.feature_type AND h.layer_id = e.layer_id AND id(f.g) = e.topogeo_id AND h.schema_name = 'ga'""")
                rows = cur.fetchall()
                
                # return all results
                lineIds = []
                for row in rows:
                    lineIds.append({'lineId': row[0], 'edgeId': row[1]})
                
                #self.db_connection_close()
                
                return lineIds
            
    def get_geometry_for_nodeid(self, nodeId):
        '''
        returns the geometry of a topo node with the given nodeId
        '''
        if nodeId:
            conn = self.db_connection(None, None, None, None)
            if conn:
                nodeGeom = None
                cur = conn.cursor()
                nodeTableName = "gas_topo.node"
                cur.execute("""SELECT ST_AsText(e.geom) from """ + nodeTableName + """ e WHERE e.node_id = """ + str(nodeId))
                rows = cur.fetchall()
                
                # should be only one
                if len(rows) > 0:
                    nodeGeom = rows[0][0]
                    
                # close connection
                #self.db_connection_close()
                
                return nodeGeom
            
                