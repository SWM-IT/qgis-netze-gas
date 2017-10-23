'''
Created on 20.10.2017

@copyright: https://gis.stackexchange.com/questions/156373/how-to-get-postgis-db-name-from-qgis-layer
@author: fischerh
'''

from __builtin__ import str
import re

class LayerDbInfo:
    def __init__(self, layerInfo):
        if layerInfo[:7] == 'service':
            layerInfo = layerInfo.replace('\'','"')
            vals = dict(re.findall('(\S+)="?(.*?)"? ',layerInfo))
            self.service = str(vals['service'])
            self.srid = int(vals['srid'])
            self.key = str(vals['key'])
            self.sql = str(vals['sql'])
            self.sslmode = str(vals['sslmode'])
            self.type = str(vals['type'])
            
            # need some extra processing to get table name and schema
            table = vals['table'].split('.')
            self.schemaName = table[0].strip('"')
            self.tableName = table[1].strip('"')
        else:
            return

    def getService(self):
        return self.service

    def getSRID(self):
        return self.srid

    def getKey(self):
        return self.key

    def getSQL(self):
        return self.sql

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
    