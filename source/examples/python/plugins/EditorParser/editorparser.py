# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EditorParser
                                 A QGIS plugin
 EditorParser
                              -------------------
        begin                : 2017-09-14
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
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from PyQt5.QtWidgets import QMessageBox, QAction, QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtXml import *
from PyQt5 import QtGui

from qgis.core import *
from qgis.gui import *

# Initialize Qt resources from file resources.py
# import resources

# Import the code for the dialog
from .editorparser_dialog import EditorParserDialog
# Import the DBConnection class
from .DBConnection import DBConnection

import os.path


class EditorParser:
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
            'EditorParser_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = EditorParserDialog()
        # set reference to db connection class
        self.Connector = DBConnection()

        self.dlg.lineEditProjectPath.clear()
        self.dlg.OperationStatments.clear()

        # set Buttens and dialogs
        self.dlg.FileDialogButtonn.clicked.connect(self.select_input_file)
        self.dlg.ConvertProjectDataButton.clicked.connect(self.start_convert)
        self.dlg.DirectConvertProjectDataButton.clicked.connect(self.start_direct_convert)

        # read smallworld page visibitiys from db
        self.editor_visibility_layers = self.get_smallworld_page_visibility()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&EditorParser')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'EditorParser')
        self.toolbar.setObjectName(u'EditorParser')

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
        return QCoreApplication.translate('EditorParser', message)

    def not_changeable_fields(self):
        field_names = {"geaendert_am": "", "erfasst_am": "", "erfasst_von": "", "geaendert_von": "", "system_id": ""}
        return field_names

    def start_convert(self):
        # clear statments dialog
        self.dlg.OperationStatments.clear()
        # read project data file
        self.read_project_data_file()
        if self.dlg.lineEditProjectPath.text() == "":
            self.show_message("ACHTUNG", "Bitte erst eine Projektdatei auswählen")
        else:

            # new project Data Name and Path
            project_data_name = self.filename.split(".qgs")
            new_project_data_name = project_data_name[0] + "_NEU.qgs"

            for layer in self.read_layers():

                # print ("NAME " + layer.name())

                if not layer.name().startswith(
                        'swb'):  # and not layer.name().startswith('G') and not layer.name().startswith('node') and not layer.name().startswith('edge'):

                    layer_element = layer.name().split(".")
                    layername = layer_element[0]

                    external_layername = self.Connector.get_external_layername(layername)

                    if external_layername == "":
                        continue
                        ### get continue with next element

                    external_name = external_layername.encode('utf-8', 'ignore').decode('utf-8')

                    # get stored visibilitys
                    if layername in self.editor_visibility_layers:
                        editor_visibility = self.editor_visibility_layers[layername]
                        # hole den richigen Maplayer vom derzeiten Layer und schreibe die Editor Sichtbarkeiten
                        self.convert_process_data(layer, editor_visibility, new_project_data_name)
                    else:
                        print("Sichtbarkeit zu " + layername + " nicht gefunden.")
            reply = QMessageBox.question(self.iface.mainWindow(), 'ACHTUNG:', 'Es wird eine neue Projekdatei angelegt!',
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # self.writeProjectDataFile()
                self.show_message("Speichern", "Projektdatei unter " + new_project_data_name + " erstellt")
            else:
                print("Projekt wurde nicht gespeichert!")

    def start_direct_convert(self):
        # clear statments dialog
        self.dlg.OperationStatments.clear()
        reply = QMessageBox.question(None, "ACHTUNG:", "Es wird die aktuelle Projekdatei angepasst!", QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # get all my project layers
            for layer in self.read_layers():
                if not layer.name().startswith(
                        'swb'):  # and not layer.name().startswith('G') and not layer.name().startswith('node') and not layer.name().startswith('edge'):
                    layer_element = layer.name().split(".")
                    layername = layer_element[0]
                    external_layername = self.Connector.get_external_layername(layername)
                    if external_layername != "":
                        external_name = external_layername.encode('utf-8', 'ignore').decode('utf-8')
                        if layername in self.editor_visibility_layers:
                            editor_visibility = self.editor_visibility_layers[layername]
                            # hole den richigen Maplayer vom derzeiten Layer und schreibe die Editor Sichtbarkeiten
                            self.direct_convert_process_data(layer, editor_visibility)
                        else:
                            print("Sichtbarkeit zu " + layername + " nicht gefunden.")
            self.show_message("Info", "Konvertierung abgeschlossen.")
        else:
            self.show_message("Abbruch", "Abbruch durch Benutzer")

    def read_project_data_file(self):
        filename = self.dlg.lineEditProjectPath.text()
        if filename == "":
            self.show_message("ACHTUNG", "keine Projektdatei ausgewählt")
            return
        else:
            tree = ET.parse(filename)
            root = tree.getroot()
            self.root_XML = root
            self.tree = tree
            print("Projektdatei eingelesen")

    def convert_process_data(self, layer, editor_visibility, new_project_data_name):
        # operation Text
        operation = []
        project_layer_name = layer.name()
        # get all field names from layer
        layer_field_names = {}
        for layer_field_name in layer.fields():
            # print(layer_field_name.name())
            layer_field_names[layer_field_name.name()] = layer_field_name

        for a_maplayer in self.root_XML.getiterator('maplayer'):
            # layername
            id_tag = a_maplayer.find('id')
            layername_tag = a_maplayer.find('layername')
            if layername_tag.text == project_layer_name:
                # split layernames behind point
                layernames = layername_tag.text.split(".")
                layername = layernames[0]
                # print("LAYERNAME " + layername)
                if not layername.startswith(
                        'swb'):  # and not layername.startswith('G') and not layername.startswith('edge') and not layername.startswith('node'):
                    #### AUSAGBE MELDUNGSFENSTER
                    operation.append("Layer " + layername + " wird bearbeitet:")
                    operation.append(".......OK")
                    self.dlg.OperationStatments.addItems(operation)
                    #### AUSGABE
                    external_layername = self.Connector.get_external_layername(layername)
                    if external_layername == "":
                        continue
                        ## get continue with next value
                    layername_tag = a_maplayer.find('layername')
                    layername_tag.text = external_layername
                    editorLayout_tag = a_maplayer.find('editorlayout')
                    editorLayout_tag.text = "tablayout"

                    # set shortname metadata for original layername
                    # if shortname tag exists
                    shortName_tag = a_maplayer.find('shortname')

                    if shortName_tag != None:
                        shortName_tag.text = layername
                    else:
                        datasource_tag = a_maplayer.find('datasource')
                        datasource_index = a_maplayer.getchildren().index(datasource_tag)
                        if datasource_index != None:
                            datasource_index = datasource_index + 1
                            newElement = ET.Element('shortname')  # create new Element
                            newElement.text = layername  # set layername to new Element shortname
                            a_maplayer.insert(datasource_index,
                                              newElement)  # insert the new Element on new element index
                    ######

                    element_index = a_maplayer.getchildren().index(
                        editorLayout_tag)  # get index number from child editorLayout
                    element_index = element_index + 1

                    newElement = ET.Element('attributeEditorForm')  # create new Element
                    a_maplayer.insert(element_index, newElement)  # insert the new Element on new element index

                    parent = a_maplayer.find('attributeEditorForm')

                    store_page_name = "main_page"
                    for visibilty in editor_visibility:

                        visibility_name = visibilty[0]

                        # schauen ob mein Feld aus in den Meta Daten der SMallworld DB steht
                        if visibility_name in layer_field_names:

                            # get index from attribute field
                            internal_fieldname = visibilty[0]
                            page_name = visibilty[1]
                            external_page_name = visibilty[2]
                            order_number = visibilty[3]
                            external_fieldname = visibilty[4]
                            field_type = visibilty[5]
                            enum_name = visibilty[6]

                            # not changeable fields
                            not_changeable_fields = {"geaendert_am": "", "erfasst_am": "", "erfasst_von": "",
                                                     "geaendert_von": ""}

                            # Datumsfelder setzen
                            if field_type == "date" or visibility_name in not_changeable_fields:

                                edittypes_tag = a_maplayer.find('edittypes')

                                for edittype in edittypes_tag.iter('edittype'):

                                    field_name = edittype.get('name')

                                    if visibility_name == field_name:

                                        widgetv2config_tag = edittype.find('widgetv2config')

                                        if field_type == "date":
                                            # setze Feldformat DateTime
                                            edittype.set('widgetv2type', "DateTime")
                                            widgetv2config_tag.set('calendar_popup', '1')
                                            widgetv2config_tag.set('display_format', 'dd.MM.yyyy')
                                            widgetv2config_tag.set('field_format', 'dd.MM.yyyy')
                                            widgetv2config_tag.set('allow_null', '1')  # erlaubt Leerwerte

                                        if visibility_name in not_changeable_fields:
                                            widgetv2config_tag.set('fieldEditable', '0')  # nicht änderbar

                            # Enumerator Felder und Werte setzen
                            if enum_name != None:

                                enum_values = self.Connector.get_enum_values(enum_name)

                                edittypes_tag = a_maplayer.find('edittypes')

                                for edittype in edittypes_tag.iter('edittype'):

                                    field_name = edittype.get('name')

                                    if visibility_name == field_name:

                                        # setze Feldformat ValueMap
                                        edittype.set('widgetv2type', "ValueMap")

                                        widgetv2config_tag = edittype.find(
                                            'widgetv2config')  # löschen und neu erstellen
                                        edittype.remove(widgetv2config_tag)

                                        Widgetv2ConfigAttributes = {"fieldEditable": "1", "constraint": "",
                                                                    "labelOnTop": "0", "constraintDescription": "",
                                                                    "notNull": "0"}

                                        # wieder neu mit standartwerten einfügen
                                        child_edittpe = ET.SubElement(edittype, "widgetv2config",
                                                                      Widgetv2ConfigAttributes)

                                        for row in enum_values:
                                            value = row[0]
                                            sequence_number = row[1]

                                            # ValueAttributes = {"key": str(sequence_number), "value": value}
                                            ValueAttributes = {"key": value, "value": value}
                                            ET.SubElement(child_edittpe, "value", attrib=ValueAttributes)

                            # get fieldIndexNumber from QGIS field
                            idx = layer.dataProvider().fieldNameIndex(layer_field_names[visibility_name].name())

                            # MAKE TAB GENERATED FIELS
                            FieldAttributes = {"index": str(idx), "name": internal_fieldname, "showLabel": "1"}

                            if page_name == "main_page":

                                ET.SubElement(parent, "attributeEditorField", attrib=FieldAttributes)

                            else:

                                if page_name != store_page_name:
                                    # make TAB Tag
                                    ContainerAttributes = {"name": external_page_name, "showLabel": "1",
                                                           "visibilityExpressionEnabled": "0",
                                                           "visibilityExpression": "", "groupBox": "0",
                                                           "columnCount": "1"}
                                    child = ET.SubElement(parent, "attributeEditorContainer",
                                                          attrib=ContainerAttributes)

                                ET.SubElement(child, "attributeEditorField", attrib=FieldAttributes, )

                            store_page_name = page_name
                            # MAKE TAB GENERATED FIELS

                            ## set aliases Names for attributs
                            aliases_tag = a_maplayer.find('aliases')

                            # gehe über die aliase Attribute und ändere die Namen mit denen aus der DB
                            for alias in aliases_tag.iter('alias'):

                                field_name = alias.get('field')
                                if visibility_name == field_name:
                                    alias.set('name', external_fieldname)

        self.tree.write(new_project_data_name)  # pretty_print=True

    def direct_convert_process_data(self, layer, editor_visibility):

        # operation Text
        operation = []

        # get all field names from layer
        layer_field_names = {}
        for layer_field_name in layer.fields():
            layer_field_names[layer_field_name.name()] = layer_field_name

        layername = layer.name()
        layernames = layername.split(".")
        layername = layernames[0]

        external_layer_name = self.Connector.get_external_layername(layername)

        doc = QDomDocument()
        map_layer = doc.createElement("maplayer")
        # write active layer xml
        layer.writeLayerXml(map_layer, doc, QgsReadWriteContext())
        layout = map_layer.firstChildElement("editorlayout")

        # set layername to QGIS
        layername_tag = map_layer.firstChildElement("layername")
        layername_tag.firstChild().setNodeValue(external_layer_name)
        #####

        # remove old attributeEditorForm Element if exists
        if map_layer.firstChildElement("datasource").nextSibling().nodeName() == "shortname":
            map_layer.removeChild(map_layer.firstChildElement("shortname").nextSibling())

        datasource = map_layer.firstChildElement("datasource")
        # shortname neu anlegen und positionieren
        newShortNameForm = doc.createElement("shortname")
        newShortNameForm.setNodeValue(layername)

        map_layer.insertAfter(newShortNameForm, datasource)

        # funktioniert noch nicht !!!
        # set shortname metadata for original layername
        # if map_layer.firstChildElement("datasource").nextSibling().nodeName() == "keywordList":

        # shortname neu anlegen und positionieren
        # newShortNameForm = doc.createElement("shortname")

        # datasource_tag = map_layer.firstChildElement("datasource")
        # datasource_tag.setNodeValue(layername)

        #  map_layer.insertAfter(newShortNameForm, datasource_tag)

        # elif map_layer.firstChildElement("datasource").nextSibling().nodeName() == "shortname":

        #   shortname_tag = map_layer.firstChildElement("shortname")
        #  shortname_tag.setNodeValue(layername)

        ####

        newAttributeEditorForm = doc.createElement("attributeEditorForm")

        # remove old attributeEditorForm Element if exists
        if map_layer.firstChildElement("editorlayout").nextSibling().nodeName() == "attributeEditorForm":
            map_layer.removeChild(map_layer.firstChildElement("editorlayout").nextSibling())

        map_layer.insertAfter(newAttributeEditorForm, layout)
        layout.firstChild().setNodeValue("tablayout")

        store_page_name = "main_page"

        for visibilty in editor_visibility:

            operation = []

            visibility_name = visibilty[0]

            idx = None
            if visibility_name in layer_field_names:

                # get index from attribute field
                internal_fieldname = visibilty[0]
                page_name = visibilty[1]
                external_page_name = visibilty[2]
                order_number = visibilty[3]
                external_fieldname = visibilty[4]
                field_type = visibilty[5]
                enum_name = visibilty[6]

                visibility_values = {"internal_fieldname": internal_fieldname, "page_name": page_name,
                                     "external_page_name": external_page_name, "external_fieldname": external_fieldname,
                                     "field_type": field_type, "enum_name": enum_name}
                print( visibility_values)
                # print("AUSGABE " + visibility_values[ external_fieldname ] )
                # get fieldIndexNumber from QGIS field
                idx = layer.dataProvider().fieldNameIndex(layer_field_names[visibility_name].name())

                # not changeable fields
                not_changeable_fields = {"geaendert_am": "", "erfasst_am": "", "erfasst_von": "", "geaendert_von": "",
                                         "system_id": ""}

                if field_type == "date" or visibility_name in not_changeable_fields:

                    edittypes_tag = map_layer.firstChildElement("edittypes")
                    # get childs editytype from edittypes Tag
                    edittypes_nodes = edittypes_tag.childNodes()

                    for i in range(0, edittypes_nodes.size()):
                        # nodes.at(i).toElement().text() # Inhalt
                        edittype_tag = edittypes_nodes.at(i).toElement()
                        name_value = edittype_tag.attribute("name")  # get value from attr name

                        if visibility_name == name_value:

                            # delete child widgetv2config from edittype tag
                            edittype_tag.removeChild(
                                edittypes_nodes.at(i).toElement().firstChildElement("widgetv2config"))

                            # make a new children widgetv2config Tag for parent edittype
                            newWidgetV2Config = doc.createElement("widgetv2config")

                            if field_type == "date":
                                # set new value to attribute widgetv2type
                                edittype_tag.setAttribute("widgetv2type", "DateTime")

                                newWidgetV2Config.setAttribute("calendar_popup", "1")
                                newWidgetV2Config.setAttribute("display_format", "dd.MM.yyyy")
                                newWidgetV2Config.setAttribute("field_format", "dd.MM.yyyy")
                                newWidgetV2Config.setAttribute('allow_null', '1')  # erlaubt Leerwerte

                                # if visibility_name =="geaendert_am" or visibility_name =="erfasst_am":
                            if visibility_name in not_changeable_fields:
                                newWidgetV2Config.setAttribute("fieldEditable",
                                                               "0")  # Feld nicht änderbar

                            edittype_tag.appendChild(newWidgetV2Config)

                            # Enumerator Felder und Werte setzen
                if enum_name != None:

                    enum_values = self.Connector.get_enum_values(enum_name)

                    edittypes_tag = map_layer.firstChildElement("edittypes")
                    # get childs editytype from edittypes Tag
                    edittypes_nodes = edittypes_tag.childNodes()

                    for i in range(0, edittypes_nodes.size()):

                        # nodes.at(i).toElement().text() # Inhalt
                        edittype_tag = edittypes_nodes.at(i).toElement()
                        name_value = edittype_tag.attribute("name")  # get value from attr name

                        if visibility_name == name_value:

                            # set new value to attribute widgetv2type
                            edittype_tag.setAttribute("widgetv2type", "ValueMap")

                            # delete child widgetv2config from edittype tag
                            edittype_tag.removeChild(
                                edittypes_nodes.at(i).toElement().firstChildElement("widgetv2config"))

                            # make a new children widgetv2config Tag for parent edittype
                            newWidgetV2Config = doc.createElement("widgetv2config")
                            newWidgetV2Config.setAttribute("fieldEditable", "1")
                            newWidgetV2Config.setAttribute("constraint", "")
                            newWidgetV2Config.setAttribute("labelOnTop", "0")
                            newWidgetV2Config.setAttribute("constraintDescription", "")
                            newWidgetV2Config.setAttribute("notNull", "0")
                            # set enum name to identify for later
                            newWidgetV2Config.setAttribute("enum_name", enum_name)

                            edittype_tag.appendChild(newWidgetV2Config)

                            # sets each enumerator value as new value tag
                            for row in enum_values:
                                value = row[0]
                                sequence_number = row[1]

                                newValue = doc.createElement("value")
                                newValue.setAttribute("key", value)
                                newValue.setAttribute("value", value)
                                # set enum name to identify for later
                                newValue.setAttribute("enum_name", enum_name)

                                newWidgetV2Config.appendChild(newValue)

                                ## Formulare generieren
                if page_name == "main_page":

                    # alleinstehendes Attribut
                    newEditorField = doc.createElement("attributeEditorField")
                    newEditorField.setAttribute("showLabel", "1")
                    newEditorField.setAttribute("index", str(idx))
                    newEditorField.setAttribute("name", internal_fieldname)

                    newAttributeEditorForm.appendChild(newEditorField)
                else:

                    # set new TabBox
                    if page_name != store_page_name:
                        # Tabbox
                        newEditorContainer = doc.createElement("attributeEditorContainer")
                        newEditorContainer.setAttribute("showLabel", "1")
                        newEditorContainer.setAttribute("visibilityExpressionEnabled", "0")
                        newEditorContainer.setAttribute("visibilityExpression", "")
                        newEditorContainer.setAttribute("name", external_page_name)
                        newEditorContainer.setAttribute("groupBox", "0")
                        newEditorContainer.setAttribute("columnCount", "1")

                        newAttributeEditorForm.appendChild(newEditorContainer)

                    newEditorField = doc.createElement("attributeEditorField")
                    newEditorField.setAttribute("showLabel", "1")
                    newEditorField.setAttribute("index", str(idx))
                    newEditorField.setAttribute("name", internal_fieldname)

                    newEditorContainer.appendChild(newEditorField)

                store_page_name = page_name

            ## set aliases Names for attributes
            if idx is not None:
                map_layer = self.write_aliases_tags(idx, visibility_name, visibility_values, map_layer, doc)

            #### AUSAGBE MELDUNGSFENSTER
        operation.append("Layer " + layername + " wird bearbeitet:")
        operation.append(".......OK")
        self.dlg.OperationStatments.addItems(operation)
        #### AUSGABE

        # write new DomElement to current active layer
        layer.readLayerXml(map_layer,QgsReadWriteContext())

    def write_aliases_tags(self, idx, visibility_name, visibility_values, map_layer, doc):

        aliases_tag = map_layer.firstChildElement("aliases")

        # get childs from aliases Tag
        nodes = aliases_tag.childNodes()

        for i in range(0, nodes.size()):
            # nodes.at(i).toElement().text() # Inhalt
            alias = nodes.at(i).toElement()
            field_value = alias.attribute("field")
            index_value = alias.attribute("index")  # we take str(idx)

            if visibility_name == field_value:
                my_node = nodes.at(i)

                FieldAttributes = {"field": field_value, "index": str(idx),
                                   "name": visibility_values["external_fieldname"]}
                #  QDomDocument / actual node / parent tag / new Subelement Name / Attributes Subelement / remove actual node
                self.create_new_element_tag(doc, my_node, aliases_tag, "alias", FieldAttributes, "true")

                # alleinstehendes Attribut
                # newAliasElement = doc.createElement("alias")
                # newAliasElement.setAttribute("field", field_value)
                # newAliasElement.setAttribute("index", str(idx))
                # newAliasElement.setAttribute("name", external_fieldname)

                # aliases_tag.appendChild(newAliasElement)

        return map_layer

    def create_new_element_tag(self, doc, my_node, parent_tag, subelement_name, attributes, remove):

        if remove:
            # delete actual alias child and make a new one
            parent_tag.removeChild(my_node)

            ## create new element
        newElement = doc.createElement(subelement_name)

        for key, val in attributes.items():
            newElement.setAttribute(key, val)

        parent_tag.appendChild(newElement)

    def read_layers(self):
        # read my project Layers from project
        layers = [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()]
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
        return QCoreApplication.translate('EditorModifier', message)

    # open file dialog for project data
    def select_input_file(self):
        project_path = QgsProject.instance().readPath("./")
        # TODO set to .qgs and .qgz --> qgz endet mit abbruch, da xml parser auf qgs gesetzt wird
        #self.filename,_ = QFileDialog.getOpenFileName(self.dlg, "Open File Dialog", project_path, "*.qgz;;*.qgs")
        self.filename,_ = QFileDialog.getOpenFileName(self.dlg, "Open File Dialog", project_path, "*.qgs")
        self.dlg.lineEditProjectPath.setText(self.filename)

    def get_smallworld_page_visibility(self):
        #
        # get editor page visibility from table gced_editorpagefield

        print("Load Smallworld PageVisibility")
        projectLayers = self.read_layers()
        # connection = self.Connector.db_connection(None, None, None, None)
        # cur = connection.cursor()

        editor_visibility_layers = {}
        for layer in projectLayers:

            layer_element = layer.name().split(".")
            table_name = layer_element[0]

            visibility_properties = self.Connector.get_visibilities_from_db(table_name)

            editor_visibiltiy = []
            for row in visibility_properties:
                internal_fieldname = row[0]  # internal fieldname
                page_name = row[1]  # page name
                external_page_name = row[2]  # external pagename
                order_number = row[3]  # order number
                external_fieldname = row[4]  # external fieldname
                field_type = row[5]  # field type
                enum_name = row[6]  # enumerator name see table gced_enum

                editor_visibiltiy.append(
                    [internal_fieldname, page_name, external_page_name, order_number, external_fieldname, field_type,
                     enum_name])

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

        icon_path = ':/plugins/EditorParser/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'EditorParser'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr(u'&EditorParser'),
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
