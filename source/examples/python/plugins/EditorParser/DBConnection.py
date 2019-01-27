'''
Created on 05.10.2017
@author: Thomas Starke, Sebastian Schmidt
'''
import psycopg2
from PyQt5.QtWidgets import QMessageBox
from .Visibililty import Visibility
from .Join import Join
import os
import configparser



class DBConnection():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Connection
        '''
        self.connection = None
        self.configFilePath = os.path.join(os.path.dirname(__file__), 'config.cfg')

    def readConfiguration(self, filePath=None):
        if filePath is None:
            filePath = self.configFilePath
        config = configparser.ConfigParser()
        config.read(filePath)
        section = 'Connection'
        host = config.get(section, 'host', fallback='localhost')
        port = config.getint(section,'port',fallback=5432)
        dbname = config.get(section,'dbname',fallback='postgres')
        user = config.get(section,'user',fallback='postgres')
        password = config.get(section,'password',fallback='postgres')
        return host,port,dbname,user,password

    def db_connection(self, host, dbname, user, password):
        # DB CONNECTION
        if not self.connection:
            host,port,dbname,user,password = self.readConfiguration()
            #TODO use port from settings
            try:
                conn = psycopg2.connect(
                    "dbname='" + dbname + "' user='" + user + "' host='" + host + "' password='" + password + "'")
                # print("DB connection ok")
                self.connection = conn
                return conn
            except:
                QMessageBox.critical(None, "Achtung", "Konnte keine Datenbankverbindung herstellen!")
                # print("I am unable to connect to the database")
        else:
            return self.connection

    def db_connection_close(self):
        '''
        close the connection to the database
        '''
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_external_layername(self, layer_name, schema):
        connection = self.db_connection(None, None, None, None)

        if connection:
            cur = connection.cursor()
            # get external layer names from database
            cur.execute("""SELECT external from """ + schema +""".gced_type WHERE name='""" + layer_name + """'""")
            row = cur.fetchone()
            self.db_connection_close()
            if row is None:
                return ""
            elif len(row) == 0:
                return ""
            else:
                return row[0]

    def get_enum_values(self, enum_name, schema):
        connection = self.db_connection(None, None, None, None)
        if connection:
            cur = connection.cursor()
            cur.execute(
                """SELECT value, sequence_number from """ + schema + """.gced_enum WHERE name='""" + enum_name + """' ORDER BY sequence_number""")
            rows = cur.fetchall()
            self.db_connection_close()
            return rows

    def get_visibilities_from_db(self, table_name, schema):
        connection = self.db_connection(None, None, None, None)
        if connection:
            cur = connection.cursor()
            cur.execute(
                """SELECT e.field_name, e.editorpage_name, e.external_page, e.order_number, f.external, f.field_type, f.enum_name from """ + schema + """.gced_editorpagefield e, """ + schema + """.gced_field f WHERE f.type_name = e.type_name AND f.name=e.field_name AND e.type_name='""" + table_name + """'  AND (e.editorpage_name='main_page' or e.editorpage_name LIKE 'sub_page%') GROUP BY e.field_name, f.external,e.editorpage_name, e.external_page, e.order_number, f.field_type, f.enum_name  ORDER BY e.editorpage_name, e.order_number""")
            rows = cur.fetchall()
            self.db_connection_close()
            visibilities = []
            for row in rows:
                visibilities.append(Visibility(row[0],row[1], row[2], row[3], row[4], row[5], row[6]))
            return visibilities

    def get_1toN_joins_from_db(self, table_name, schema):
        connection = self.db_connection(None, None, None, None)
        print("table: " + table_name)
        print("schema: " + schema)
        if connection:
            cur = connection.cursor()
            cur.execute(
                "SELECT f.type_name as own_table, from_mapping_fields as own_field, result_name as foreign_table, to_mapping_fields as foreign_field, \"external\" as external_name FROM " + schema + ".gced_field f WHERE f.field_type = 'join' AND f.type_name= '" + table_name + "' and result_type = 'single'")
            rows = cur.fetchall()
            self.db_connection_close()
            print("result from getJoins")
            print(rows)
            joins = []
            for row in rows:
                joins.append(Join(row[0],row[1],row[2],row[3],row[4]))
            return joins
