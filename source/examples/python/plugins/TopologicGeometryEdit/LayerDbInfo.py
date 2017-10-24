'''
Created on 20.10.2017

@copyright: https://gis.stackexchange.com/questions/156373/how-to-get-postgis-db-name-from-qgis-layer
@author: fischerh
'''

from __builtin__ import str
import re

class LayerDbInfo:
    def __init__(self, layerInfo):
        if layerInfo[:6] == 'dbname':
            layerInfo = layerInfo.replace('\'','"')
            vals = dict(re.findall('(\S+)="?(.*?)"? ',layerInfo))
            self.dbName = str(vals['dbname'])
            self.host = str(vals['host'])
            self.port = int(vals['port'])
            self.user = str(vals['user'])
            self.password = str(vals['password'])
            self.srid = int(vals['srid'])
            self.sslmode = str(vals['sslmode'])
            self.type = str(vals['type'])
            
            # need some extra processing to get table name and schema
            table = vals['table'].split('.')
            self.schemaName = table[0].strip('"')
            self.tableName = table[1].strip('"')
        else:
            return

    def getDbName(self):
        return self.dbName
    
    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port
    
    def getUser(self):
        return self.user
    
    def getPassword(self):
        return self.password
    
    def getSRID(self):
        return self.srid

    def getSSLmode(self):
        return self.sslmode

    def getType(self):
        return self.type

    def getSchema(self):
        return self.schemaName

    def getTable(self):
        return self.tableName
    
    def getFullTableName(self):
        return self.schemaName + "." + self.tableName
    