'''
Created on 15.09.2017

@author: fischerh
'''
import psycopg2
from PyQt4.QtGui import QMessageBox
from platform import node

class TopologyConnector():
    '''
    classdocs
    '''


    def __init__(self, host, dbname, user, password):
        '''
        Constructor
        '''
        self.connection = self.db_connection(host, dbname, user, password)
        
    def db_connection(self, host, dbname, user, password):
        '''
        returns a database connection with given parameter
        '''
        toolname = "TopologyConnector"
        
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
            return conn
        except:
            # show error
            QMessageBox.critical(None, toolname, "There was an error connecting to the database.")
            
    def all_edges_for_node(self, nodeId):
        '''
        returns all connected edges to a node
        '''
        
    def all_nodes_for_edge(self, edgeId):
        '''
        returns all connected nodes to an edge
        '''
        
    