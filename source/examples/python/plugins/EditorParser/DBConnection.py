'''
Created on 15.09.2017
@author: fischerh
'''
import psycopg2
from PyQt4.QtGui import QMessageBox
from platform import node

class DBConnection():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Connection
        '''
        self.connection = None
        
    

    def db_connection(self, host, dbname, user, password):
        
            ## DB CONNECTION   
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
                #print  "DB connection ok"
                self.connection = conn
                return conn

            except:
                
                QMessageBox.critical(None, "Achtung", "Konnte keine Datenbankverbindung herstellen !!")
                #print "I am unable to connect to the database"
        else:
            
            return self.connection 
        
        
    def db_connection_close(self):
        '''
        close the connection to the database
        '''
        if self.connection:
            self.connection.close()
            self.connection = None     
            
            
    def getExternalLayername(self, layername):             
        
        connection = self.db_connection(None, None, None, None)                   
                    
        if connection:
            
            cur = connection.cursor()
            
            # get external layer names from database
            cur.execute("""SELECT external from ga.gced_type WHERE name='""" + layername + """'""")
            row = cur.fetchone()
            
            self.db_connection_close() 
        
            return row[0]
        
        
    def getEnumValues(self, enum_name):

        connection = self.db_connection(None, None, None, None)                   
                    
        if connection:
            
            cur = connection.cursor()
        
            cur.execute("""SELECT value, sequence_number from ga.gced_enum WHERE name='""" + enum_name + """' ORDER BY sequence_number""")
            rows = cur.fetchall()
            
            self.db_connection_close() 
            
            return rows 

     

    def getVisibilitysFromDB(self, table_name):        
      
        connection = self.db_connection(None, None, None, None)               
                  
        if connection:
        
            cur = connection.cursor()
        
            cur.execute("""SELECT e.field_name, e.editorpage_name, e.external_page, e.order_number, f.external, f.field_type, f.enum_name from ga.gced_editorpagefield e, ga.gced_field f WHERE f.type_name = e.type_name AND f.name=e.field_name AND e.type_name='""" + table_name + """'  AND (e.editorpage_name='main_page' or e.editorpage_name LIKE 'sub_page%') GROUP BY e.field_name, f.external,e.editorpage_name, e.external_page, e.order_number, f.field_type, f.enum_name  ORDER BY e.editorpage_name, e.order_number""")
            rows = cur.fetchall()
            
            self.db_connection_close() 
            
            return rows

