# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EditorModifierSql
                                 A QGIS plugin
 Editor modifier SQL
                              -------------------
        begin                : 2017-09-12
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Thomas Starke
        email                : thomas.starke@mettenmeier.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4 import QtGui

from qgis.core import *
from qgis.gui import *

import psycopg2

import xml.etree.ElementTree as ET
#from xml.etree.ElementTree import Element, SubElement, Comment
#from ElementTree_pretty import prettify

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from editor_modifier_dialog import EditorModifierSqlDialog
import os.path


class EditorModifierSql:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'EditorModifierSql_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
         
        # Create the dialog (after translation) and keep reference
        self.dlg = EditorModifierSqlDialog()        
        
        self.dlg.lineEditProjectPath.clear()
        self.dlg.OperationStatments.clear()       
        
        # Buttens
        self.dlg.FileDialogButton.clicked.connect(self.select_input_file)  
        self.dlg.ConvertProjectDataButton.clicked.connect(self.startConvert) 
         
        # make DB Connection        
        self.db_connection = self.make_db_connection()   
       
        if self.db_connection:
            
            # get project Layer Names
            self.projectLayers = self.readLayers()
            
            # get smallworld visibitlity from postgress DB for each project layer
            self.editor_visibility_layers = self.get_smallworld_PageVisibility(self.projectLayers)   
            
            
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Editor modifier SQL')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'EditorModifierSql')
        self.toolbar.setObjectName(u'EditorModifierSql')
        
        
        
    def startConvert(self):
        
        # read project data file
        self.readProjectDataFile()     
   
        
        if self.dlg.lineEditProjectPath.text() == "":
            
            self.show_message("ACHTUNG", "Erst eine Projektdatei ausw�hlen")
        
        else: 
                      
            conn = self.db_connection
            cur = conn.cursor()
              
            # new project Data Name and Path  
            project_data_name = self.filename.split(".qgs")
            new_project_data_name = project_data_name[0] + "_NEU.qgs" 
        
            for layer in self.iface.legendInterface().layers():
            
                #print ("NAME " + layer.name()) 
            
                if not layer.name().startswith('swb') and not layer.name().startswith('G'):            
            
                    layer_element = layer.name().split(".")
                    layername = layer_element[0] 
                
                    # get external layer names from database
                    cur.execute("""SELECT external from ga.gced_type WHERE name='""" + layername + """'""")
                    row = cur.fetchone()
                        
                    external_name = row[0].encode('utf-8', 'ignore').decode('utf-8') 
                
                    # HOLE MIR DIE SICHTBARKEITEN ZUM LAYER 
                    editor_visibility = self.editor_visibility_layers[layername]
                    
                    # hole den richigen Maplayer vom derzeiten Layer und schreibe die Editor Sichtbarkeiten 
                    self.convertProcessData(layer, editor_visibility, new_project_data_name) 
                
                #else:
                   
                    #print("keine Layer zum konvertieren gefunden")
            
            
            reply = QMessageBox.question(self.iface.mainWindow(), 'ACHTUNG:', 'Es wird eine neue Projekdatei angelegt !', QMessageBox.Yes, QMessageBox.No)
        
            if reply == QtGui.QMessageBox.Yes:
            
                #self.writeProjectDataFile()
                self.show_message("Speichern", "Projektdatei unter " + new_project_data_name + " erstellt")            
            
            else:
            
                print "Projekt wurde nicht gespeichert !" 
            
        # close db connection
        #conn.close()  
          
        
    def readProjectDataFile(self):
        
        
        filename = self.dlg.lineEditProjectPath.text()         
        
         
        if filename == "":
             
            self.show_message("ACHTUNG","keine Projektdatei ausgewählt")     
            return false 
        
        else:
            
            tree = ET.parse(filename)
            root = tree.getroot()
            
            self.root_XML = root 
            self.tree = tree  
            
            print("Projektdatei eingelesen")            
        
    
    
    def convertProcessData(self, layer, editor_visibility, new_project_data_name):
        
        # operation Text
        operation = []        
        
        project_layer_name = layer.name()        
        
        # get all field names from layer
        layer_field_names = {}
      
        for layer_field_name in layer.pendingFields():
            
            #print layer_field_name.name()
            layer_field_names[ layer_field_name.name()  ] = layer_field_name            
        
        #a_maplayer = self.root_XML.findall(".//maplayer[layername='  " + project_layer_name + ']")
        # root.findall(".//maplayer/[layername='g_schutzmassnahme.flaeche']*")
                   
        for a_maplayer in self.root_XML.getiterator('maplayer'):         
          
            # jeder Layer ist in einem maplayer Tag definiert
            conn = self.db_connection
            # get editor page visibility from table gced_editorpagefield
            cur = conn.cursor()            
            
            # layername  
            id_tag = a_maplayer.find('id')
            layername_tag = a_maplayer.find('layername')  
            
            if layername_tag.text == project_layer_name:  
          
                # split layernames behind point
                layernames = layername_tag.text.split(".")
                layername = layernames[0] 

                
                if not layername.startswith('swb') and not layername.startswith('G'):                   
                    
                    #### AUSAGBE MELDUNGSFENSTER                    
                    operation.append("Layer " + layername + " wird bearbeitet:")                    
                    self.dlg.OperationStatments.addItems(operation)
                    #### AUSGABE  
            
                    print("LAYERNAME !! " + layername)    
                    
                    ##### Schreibe den Layernamen noch ausgliedern....
                    # get external layer names from database
                    cur.execute("""SELECT external from ga.gced_type WHERE name='""" + layername + """'""")
                    row = cur.fetchone()
                        
                    external_layer_name = row[0] #.encode('utf-8', 'ignore').decode('utf-8')   
                    #########
                    
                    layername_tag = a_maplayer.find('layername')  
                    #print("LAYERNAME AUS TAG " + str(layername_tag.text))
                    layername_tag.text = external_layer_name         
                               
                    editorLayout_tag = a_maplayer.find('editorlayout')
                    editorLayout_tag.text = "tablayout"
                        #print(editorLayout_tag)
                                   
                    element_index = a_maplayer.getchildren().index(editorLayout_tag) # get index number from child editorLayout
                    element_index = element_index +1
            
                    newElement =  ET.Element('attributeEditorForm') # create new Element
                    a_maplayer.insert(element_index, newElement) # insert the new Element on new element index
            
                    parent = a_maplayer.find('attributeEditorForm') 
                      
                    store_page_name = "main_page"      
                    for visibilty in editor_visibility:   
                
                        visibility_name = visibilty[0]                          
                                           
                        # schauen ob mein Feld aus in den Meta Daten der SMallworld DB steht
                        if layer_field_names.has_key(visibility_name):                            
                          
                            # get index from attribute field                                
                            internal_fieldname = visibilty[0]
                            page_name = visibilty[1] 
                            external_page_name = visibilty[2]
                            order_number = visibilty[3] 
                            external_fieldname = visibilty[4]
                            field_type = visibilty[5]
                            enum_name = visibilty[6]
                            
                            #print ("ENUM NAME " + str(enum_name))
                            
                            
                            # Datumsfelder setzen
                            if field_type == "date": 
                                
                                edittypes_tag = a_maplayer.find('edittypes') 
                                
                                for edittype in edittypes_tag.iter('edittype'):
                                
                                    field_name = edittype.get('name')
                                
                                    if visibility_name == field_name:                                        
                                        
                                        # setze Feldformat DateTime
                                        edittype.set('widgetv2type', "DateTime")
                                        
                                        widgetv2config_tag = edittype.find('widgetv2config') 
                                        
                                        widgetv2config_tag.set('calendar_popup', '1')
                                        widgetv2config_tag.set('display_format', 'dd.MM.yyyy')
                                        widgetv2config_tag.set('field_format', 'dd.MM.yyyy')
                                        
                            # Enumerator Werte setzen
                            if enum_name != None:
                                
                                # hole mir die Daten aus der Datenbank
                                cur.execute("""SELECT value, sequence_number from ga.gced_enum WHERE name='""" + enum_name + """' ORDER BY sequence_number""")
                                rows = cur.fetchall()
                                
                                edittypes_tag = a_maplayer.find('edittypes') 
                                
                                for edittype in edittypes_tag.iter('edittype'):
                                
                                    field_name = edittype.get('name')
                                
                                    if visibility_name == field_name:                                        
                                        
                                        # setze Feldformat ValueMap
                                        edittype.set('widgetv2type', "ValueMap")
                                        
                                        widgetv2config_tag = edittype.find('widgetv2config')  # löschen und neu erstellen
                                        edittype.remove(widgetv2config_tag)
                                        
                                        # wieder neu mit standartwerten einfügen                                        
                                        child = ET.SubElement(edittype, "widgetv2config",  fieldEditable="1", constraint="", labelOnTop="0", constraintDescription="", notNull="0")
                                        
                                        for row in rows:
                                            
                                            value= row[0] #.encode('utf-8', 'ignore').decode('utf-8')   
                                            sequence_number = row[1] #.encode('utf-8', 'ignore').decode('utf-8')   
                                            
                                            ValueAttributes = {"key": str(sequence_number), "value": value}
                                            #ValueAttributes = {"key": value, "value": str(sequence_number)}
                                            ValueAttributes = {"key": value, "value": value}
                                            ET.SubElement(child, "value", attrib=ValueAttributes)
                             
                             
                            # get fieldIndexNumber from QGIS for field    
                            idx = layer.fieldNameIndex(layer_field_names[ visibility_name ].name())
                                
                            #layer.renameAttribute(idx, external_fieldname)                        
                            
                            # MAKE TAB GENERATED FIELS 
                            FieldAttributes = {"index": str(idx), "name": internal_fieldname}
                            
                            if page_name == "main_page":
                                
                                child = ET.SubElement(parent, "attributeEditorField", showLabel="1", attrib=FieldAttributes)
                            
                            else:
                                
                                if page_name != store_page_name: 
                                    
                                    ContainerAttributes = {"name": external_page_name}
                                    child = ET.SubElement(parent, "attributeEditorContainer", showLabel="1",  visibilityExpressionEnabled="0", visibilityExpression="", groupBox="0", columnCount="1", attrib=ContainerAttributes)
                                
                                ET.SubElement(child, "attributeEditorField", attrib=FieldAttributes, showLabel="1")
                            
                            store_page_name = page_name                       
                            # MAKE TAB GENERATED FIELS                             
                                       
                            #edittypes_tag = a_maplayer.find('edittypes')  
                            
                            # gehe �ber die Edittypes Attribute und �nderen die Namen mit denen aus der DB
                            ## Modifiy edittype TAGS
                            #for edittype in edittypes_tag.iter('edittype'):
                    
                            #    field_name = edittype.get('name')
                                
                            #    if visibility_name == field_name:
                                    
                            #        edittype.set('name',  external_fieldname)
                                    
                            ## Modifiy defaults TAGS     
                            #defaults_tag = a_maplayer.find('defaults') 
                            
                            # gehe �ber die Defaults Attribute und �nderen die Namen mit denen aus der DB
                            #for default in defaults_tag.iter('default'):
                    
                            #    field_name = default.get('field')
                                
                            #    if visibility_name == field_name:
                                    
                            #        default.set('field',  external_fieldname)
                                    
                                    
                            ## set aliases Names for attributs      
                            aliases_tag = a_maplayer.find('aliases') 
                                    
                            # gehe �ber die aliase Attribute und �nderen die Namen mit denen aus der DB
                            for alias in aliases_tag.iter('alias'):
                    
                                field_name = alias.get('field')
                                
                                if visibility_name == field_name:
                                    
                                    alias.set('name',  external_fieldname)                                    
                            
                    #### AUSAGBE MELDUNGSFENSTER                    
                    operation.append(".......OK")                    
                    self.dlg.OperationStatments.addItems(operation)
                    #### AUSGABE      
        
        
        self.tree.write(new_project_data_name) # pretty_print=True
        
        
    
    def readLayers(self):
        
        # read my project Layers from project  
        layers = self.iface.legendInterface().layers()       

        projectLayer = []
        for l in layers:    
                                        
            projectLayer.append(l)
      
        return projectLayer    
        

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('EditorModifierSql', message)
   
   
    # open file dialog for project data
    def select_input_file(self):     
        
        ProjectPath = QgsProject.instance().readPath("./")                           
        self.filename = QFileDialog.getOpenFileName(self.dlg, "Open File Dialog", ProjectPath, "*.qgs")
        
        self.dlg.lineEditProjectPath.setText(self.filename)  
         
    
    def make_db_connection(self):

            ## DB CONNECTION        
        try:
            conn = psycopg2.connect("dbname='nisconnect_integration' user='postgres' host='localhost' password='postgres'")
            print  "DB connection ok"
            return conn 
        except:
            print "I am unable to connect to the database"
        ####   
    
    
    def get_smallworld_PageVisibility(self, projectLayers):        
      
        #
        # get editor page visibility from table gced_editorpagefield
        
        print("Load Smallworld PageVisibility")
        
        conn = self.db_connection        
        cur = conn.cursor()
                
        editor_visibility_layers = {}
        for layer in projectLayers:
            
            layer_element = layer.name().split(".")
            table_name = layer_element[0] 
        
            cur.execute("""SELECT e.field_name, e.editorpage_name, e.external_page, e.order_number, f.external, f.field_type, f.enum_name from ga.gced_editorpagefield e, ga.gced_field f WHERE f.type_name = e.type_name AND f.name=e.field_name AND e.type_name='""" + table_name + """'  AND (e.editorpage_name='main_page' or e.editorpage_name LIKE 'sub_page%') GROUP BY e.field_name, f.external,e.editorpage_name, e.external_page, e.order_number, f.field_type, f.enum_name  ORDER BY e.editorpage_name, e.order_number""")

            rows = cur.fetchall()        
         
            editor_visibiltiy = []
            for row in rows:
           
                internal_fieldname= row[0]  # internal fieldname
                page_name = row[1]  # page name
                external_page_name = row[2] # external pagename
                order_number = row[3]  # order number
                external_fieldname = row[4] # external fieldname
                field_type = row[5]# field type
                enum_name = row[6]  # enumerator name see table gced_enum                 
            
                editor_visibiltiy.append([internal_fieldname, page_name, external_page_name, order_number,external_fieldname, field_type, enum_name])  
            
            editor_visibility_layers[table_name] = editor_visibiltiy
                 
        # get back visibility in order from meta_data tables
        return editor_visibility_layers 
    
    
    def show_message(self, title, text):
    
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec_()  
        

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToDatabaseMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/EditorModifierSql/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Editor modifier SQL'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr(u'&Editor modifier SQL'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()  
        
        
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
           # msg = QMessageBox()
       # msg.setText(self.db_connection)
           # msg.setText("TEST")
        
           # msg.show()