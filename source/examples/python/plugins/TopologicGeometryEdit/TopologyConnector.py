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
                tableName = "gas_test.edge_data"
                cur.execute("""SELECT e.edge_id from """ + tableName + """ e WHERE e.start_node = """ + str(nodeId) + """ OR e.end_node = """ + str(nodeId))
                
                rows = cur.fetchall()
                
                edgeIds = []
                
                for row in rows:
                    edgeIds.append(row[0])
                    
                # close connection
                self.db_connection_close()
                
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
        if aPointId:
            # get db connection
            conn = self.db_connection(None, None, None, None)
            if conn:
                nodeId = None
                # get db entry for point object
                # exemplary house connection table - should be retrieved from selected layer
                cur = conn.cursor()
                haTableName = "gas_test.hausanschluss"
                reTableName = "gas_test.relation"
                
                cur.execute("""SELECT f.element_id from """ + haTableName + """ e, """ + reTableName + """ f WHERE e.system_id = """ + str(aPointId) + """ AND f.topogeo_id = id(e.g) AND f.element_type = 1""")
                
                rows = cur.fetchall()
                
                # should be only one
                if rows[0]:
                    nodeId = rows[0][0]
                    
                # close connection
                self.db_connection_close()
                
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
                reTableName = "gas_test.relation"
                alTableName = "gas_test.anschlussltg_abschnitt"
                #cur.execute("""SELECT e.topogeo_id from """ + reTableName + """ e WHERE e.element_id = """ + str(edgeId) + """ AND e.element_type = 2""")
                cur.execute("""SELECT f.system_id from """ + reTableName + """ e, """ + alTableName + """ f WHERE e.element_id in (""" + ','.join(map(str, edgeIds)) + """) AND e.element_type = 2 AND id(f.g) = e.topogeo_id""")
                rows = cur.fetchall()
                
                # return all results
                lineIds = []
                for row in rows:
                    lineIds.append(row[0])
                
                self.db_connection_close()
                
                return lineIds