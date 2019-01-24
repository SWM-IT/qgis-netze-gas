'''
Created on 05.10.2017
@author: Thomas Starke, Sebastian Schmidt
'''
import psycopg2
from PyQt5.QtWidgets import QMessageBox
from .Visibililty import Visibility



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
        # DB CONNECTION
        if not self.connection:
            if not host:
                host = "nis_pool_test.intra.swm.de"
            if not dbname:
                dbname = "nisconnect_test"
            if not user:
                user = "nis_readonly"
            if not password:
                password = "yln0daer"
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