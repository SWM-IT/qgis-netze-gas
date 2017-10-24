'''
Created on 23.10.2017

@author: fischerh
'''

class TopoLine:
    def __init__(self):
        '''
        constructor
        '''
        self.systemId = None
        self.schemaName = None
        self.tableName = None # should match the  the QgsVectorLayer.shortName()
        self.topologyId = None
        self.edgeId = None
        self.fid = None
        
    def setSystemId(self, systemId):
        self.systemId = systemId
        
    def setSchemaName(self, schemaName):
        self.schemaName = schemaName
    
    def setTableName(self, tableName):
        self.tableName = tableName
        
    def setTopologyId(self, topologyId):
        self.topologyId = topologyId
        
    def setEdgeId(self, edgeId):
        self.edgeId = edgeId
        
    def setFid(self, fid):
        self.fid = fid
        
    def getSystemId(self):
        return self.systemId
    
    def getSchemaName(self):
        return self.schemaName
    
    def getTableName(self):
        return self.tableName
    
    def getFullTableName(self):
        return self.schemaName + "." + self.tableName
    
    def getTopologyId(self):
        return self.topologyId
    
    def getEdgeId(self):
        return self.edgeId
    
    def getFid(self):
        return self.fid
        