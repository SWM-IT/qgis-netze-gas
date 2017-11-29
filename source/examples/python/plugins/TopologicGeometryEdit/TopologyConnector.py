'''
Created on 15.09.2017

@author: fischerh
'''
import psycopg2
from PyQt4.QtGui import QMessageBox
from platform import node
from __builtin__ import str
from TopoLine import TopoLine
from TopoPoint import TopoPoint

class TopologyConnector():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.connection = None
        
    def db_connection(self, host="localhost", dbname="nisconnect_integration", user="postgres", password="postgres"):
        '''
        returns a database connection with given parameter
        '''
        toolname = "TopologyConnector"
        
        if not self.connection:
            '''
            if not host:
                host = "localhost"
            if not dbname:
                dbname = "nisconnect_integration"
            if not user:
                user = "postgres"
            if not password:
                password = "postgres"
            '''
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
    
    def primaryKey(self, fullTableName):
        '''
        return the primary key for fullTableName
        '''
        pKey = "system_id"
        #'''
        if fullTableName:
            conn = self.db_connection() #None, None, None, None)
            if conn:
                cur = conn.cursor()
                
                cur.execute("""SELECT pg_attribute.attname FROM pg_index, pg_class, pg_attribute WHERE pg_class.oid = '""" + str(fullTableName) + """'::regclass AND indrelid = pg_class.oid AND pg_attribute.attrelid = pg_class.oid AND pg_attribute.attnum = any(pg_index.indkey) AND indisprimary""")
                
                rows = cur.fetchall()
                
                if len(rows) == 1:
                    pKey = rows[0][0]
        
        #'''                
        return pKey 
    
    def all_edges_for_node(self, nodeId):
        '''
        returns all connected edges to a node
        '''
        if nodeId:
            # get db connection
            conn = self.db_connection() #None, None, None, None)
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
            
            
        
    def all_nodes_for_edges(self, topoEdgeData):
        '''
        returns all connected nodes to a list of edges
        '''
        edgeIds = []
        nodeIds = []
        
        for aTopoLine in topoEdgeData:
            edgeId = aTopoLine.getEdgeId()
            if edgeId:
                edgeIds.append(edgeId)
                
        if len(edgeIds) > 0:
            # get db connection
            conn = self.db_connection() #None, None, None, None)
            if conn:
                # get node entries from edge table
                cur = conn.cursor()
                tableName = "gas_topo.edge_data"
                cur.execute("""SELECT e.start_node, e.end_node from """ + tableName + """ e WHERE e.edge_id in (""" + ','.join(map(str, edgeIds)) + """)""")
                
                rows = cur.fetchall()
                nodeIds = []
                for row in rows:
                    for i in {0,1}:
                        if not row[i] in nodeIds:
                            nodeIds.append(row[i])
            
        if len(nodeIds) > 0:
            # get node geometries from relation table
            cur = conn.cursor()
            tableName = "gas_topo.node"
            cur.execute("""SELECT e.node_id, e.geom from """ + tableName + """ e WHERE e.node_id in (""" + ','.join(map(str, nodeIds)) + """)""")
                
            rows = cur.fetchall()
            nodeData = []
            
            for row in rows:
                nodeData.append({'nodeId': row[0], 'nodeGeom': row[1]})
            
        return nodeData
        
    def get_nodeData_for_point(self, aPointObject):
        '''
        returns the topology node data related to the given point object
        '''
        if self.layerDbInfo:
            gTableName = self.layerDbInfo.getTable()
            fullTableName = "ga." + gTableName
            primaryKey = self.primaryKey(fullTableName)
            aPointId = aPointObject.attribute(primaryKey)
            if aPointId:
                # get db connection
                conn = self.db_connection() #None, None, None, None)
                if conn:
                    nodeData = None
                    # get db entry for point object
                    # exemplary house connection table - should be retrieved from selected layer
                    cur = conn.cursor()
                    #haTableName = self.layerDbInfo.getFullTableName() # "ga.g_hausanschluss"
                    reTableName = "gas_topo.relation"
                    topoTableName = "topology.layer"
                    
                    cur.execute("""SELECT h.topology_id, h.schema_name, h.table_name, f.element_id from """ + fullTableName + """ e, """ + reTableName + """ f, """ + topoTableName + """ h WHERE e.""" + primaryKey + """ = """ + str(aPointId) + """ AND f.topogeo_id = id(e.g) AND f.layer_id = h.layer_id AND h.table_name = '""" + str(gTableName) + """' AND h.layer_id = layer_id(e.g) AND h.topology_id = topology_id(e.g)""")
                    
                    rows = cur.fetchall()
                    
                    # should be only one
                    if len(rows) > 0:
                        row = rows[0]
                        aTopoPoint = TopoPoint()
                        aTopoPoint.setTopologyId(row[0])
                        aTopoPoint.setSchemaName(row[1])
                        aTopoPoint.setTableName(row[2])
                        aTopoPoint.setNodeId(row[3])
                        nodeData = aTopoPoint
                    # close connection
                    #self.db_connection_close()
                    
                    return nodeData
        
    def get_edgeData_for_line(self, aLineObject):
        '''
        returns the topology edge data related to the given line object
        '''
        if self.layerDbInfo: # and aLineId:
            gTableName = self.layerDbInfo.getTable()
            fullTableName = "ga." + gTableName
            primaryKey = self.primaryKey(fullTableName)
            aLineId = aLineObject.attribute(primaryKey)
            if aLineId:
                # get db connection
                conn = self.db_connection() #None, None, None, None)
                if conn:
                    lineData = []
                    
                    cur = conn.cursor()
                    
                    reTableName = "gas_topo.relation"
                    topoTableName = "topology.layer"
                    
                    cur.execute("""SELECT h.topology_id, h.schema_name, h.table_name, f.element_id from """ + fullTableName + """ e, """ + reTableName + """ f, """ + topoTableName + """ h WHERE e.""" + primaryKey + """ = """ + str(aLineId) + """ AND f.topogeo_id = id(e.g) AND f.layer_id = h.layer_id AND h.table_name = '""" + str(gTableName) + """' AND h.layer_id = layer_id(e.g) AND h.topology_id = topology_id(e.g)""")
                    
                    rows = cur.fetchall()
                    
                    # could be more than one
                    for row in rows:
                        aTopoLine = TopoLine()
                        aTopoLine.setTopologyId(row[0])
                        aTopoLine.setSchemaName(row[1])
                        aTopoLine.setTableName(row[2])
                        aTopoLine.setEdgeId(row[3])
                        lineData.append(aTopoLine)
                    # close connection
                    #self.db_connection_close()
                    
                    return lineData
        
    def get_points_for_nodeids(self, nodeIds, topoId):
        '''
        returns the point objects related to the given node ids
        '''
        if nodeIds:
            conn = self.db_connection() #None, None, None, None)
            if conn:
                pointIds = []
                pointData = []
                cur = conn.cursor()
                reTableName = "gas_topo.relation"
                topoTableName = "topology.layer"
                cur.execute("""SELECT f.topogeo_id, h.schema_name, h.table_name, f.element_id from """ + reTableName + """ f, """ + topoTableName + """ h WHERE f.element_id in (""" + ','.join(map(str, nodeIds)) + """) AND h.topology_id = """ + str(topoId) + """ AND h.layer_id = f.layer_id and f.element_type = 1""")
                rows = cur.fetchall()
                
                for row in rows:
                    aTopoPoint = TopoPoint()
                    aTopoPoint.setTopologyId(row[0])
                    aTopoPoint.setSchemaName(row[1])
                    aTopoPoint.setTableName(row[2])
                    aTopoPoint.setNodeId(row[3])
                    pointIds.append(aTopoPoint)
                
                for aPoint in pointIds:
                    primaryKey = self.primaryKey(aPoint.getFullTableName())
                    cur = conn.cursor()
                    cur.execute("""SELECT f.""" + primaryKey + """ from """ + str(aPoint.getFullTableName()) + """ f  WHERE id(f.g) = """ + str(aPoint.getTopologyId()) )
                    row = cur.fetchone()
                    if row:
                        aPoint.setSystemId(row[0])
                        pointData.append(aPoint)
                
                return pointData
        
    def get_lines_for_edgeids(self, edgeIds, topoId):
        '''
        returns the line objects related to the given edge ids
        '''
        if edgeIds:
            conn = self.db_connection() #None, None, None, None)
            if conn:
                lineIds = []
                lineData = []
                cur = conn.cursor()
                reTableName = "gas_topo.relation"
                topoTableName = "topology.layer"
                cur.execute("""SELECT f.topogeo_id, h.schema_name, h.table_name, f.element_id from """ + reTableName + """ f, """ + topoTableName + """ h WHERE f.element_id in (""" + ','.join(map(str, edgeIds)) + """) AND h.topology_id = """ + str(topoId) + """ AND h.layer_id = f.layer_id""")
                rows = cur.fetchall()
                
                for row in rows:
                    aTopoLine = TopoLine()
                    aTopoLine.setTopologyId(row[0])
                    aTopoLine.setSchemaName(row[1])
                    aTopoLine.setTableName(row[2])
                    aTopoLine.setEdgeId(row[3])
                    #lineIds.append({'topoId': row[0], 'table': lineTableName, 'edgeId': row[3]})
                    lineIds.append(aTopoLine)
                #alTableName = "ga.g_anschlussltg_abschnitt"
                for aLine in lineIds:
                    primaryKey = self.primaryKey(aLine.getFullTableName())
                    cur.execute("""SELECT f.""" + primaryKey + """ from """ + str(aLine.getFullTableName()) + """ f  WHERE id(f.g) = """ + str(aLine.getTopologyId()) )
                    row = cur.fetchone()
                    if row:
                        aLine.setSystemId(row[0])
                        #lineData.append({'lineId': row[0], 'edgeId': aLine['edgeId'], 'lineTable': aLine['table']})
                        lineData.append(aLine)
                
                #cur.execute("""SELECT f.system_id, e.element_id, h.table_name from """ + reTableName + """ e, """ + alTableName + """ f, """ + topoTableName + """ h WHERE e.element_id in (""" + ','.join(map(str, edgeIds)) + """) AND e.element_type = h.feature_type AND h.layer_id = e.layer_id AND id(f.g) = e.topogeo_id AND h.schema_name = 'ga'""")
                #rows = cur.fetchall()
                # return all results
                #lineIds = []
                #for row in rows:
                #    lineIds.append({'lineId': row[0], 'edgeId': row[1], 'lineTable': row[2]})
                
                #self.db_connection_close()
                
                return lineData
            
    def get_geometry_for_nodeid(self, nodeId):
        '''
        returns the geometry of a topo node with the given nodeId
        '''
        if nodeId:
            conn = self.db_connection() #None, None, None, None)
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
            
                