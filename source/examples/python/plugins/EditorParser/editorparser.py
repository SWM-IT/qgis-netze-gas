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
        # Todo why does this not work when debugging?
        #locale = QSettings().value('locale/userLocale')[0:2]
        locale = 'de'
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
        self.connector = DBConnection()

        self.dlg.lineEditProjectPath.clear()
        self.dlg.OperationStatments.clear()

        # set Buttons and dialogs
        self.dlg.DirectConvertProjectDataButton.clicked.connect(self.start_direct_convert)

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

    def source_table_name(self, layer):
        # TODO exclude some metadata tables
        # if layer.name().startswith('swb'): # and not layer.name().startswith('G') and not layer.name().startswith('node') and not layer.name().startswith('edge'):
        return layer.dataProvider().uri().schema(), layer.dataProvider().uri().table()

    def start_direct_convert(self):
        # clear statements dialog
        self.dlg.OperationStatments.clear()
        reply = QMessageBox.question(None, "ACHTUNG:", "Es wird die aktuelle Projekdatei angepasst!", QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # get all my project layers
            layers = self.read_layers()
            print(layers)
            # add Relations between layers to project
            relations = []
            joins = []
            for layer in layers:
                schemaname, tablename = self.source_table_name(layer)
                joins_for_layer = self.connector.get_1toN_joins_from_db(tablename, schemaname)
                relations = self.create_relations(layer, joins_for_layer, relations)
                joins.extend(joins_for_layer)
            if relations:
                for rel in relations:
                    QgsProject.instance().relationManager().addRelation(rel)
            # Process external names layer by layer
            mapping_table = self.get_smallworld_page_visibilities(layers)
            for layer in layers:
                schemaname, tablename = self.source_table_name(layer)
                if tablename is not None:
                    external_layername = self.connector.get_external_layername(tablename,schemaname)
                    if external_layername != "":
                        external_name = external_layername.encode('utf-8', 'ignore').decode('utf-8')
                        if tablename in mapping_table:
                            editor_visibility = mapping_table[tablename]
                            # hole den richigen Maplayer vom derzeiten Layer und schreibe die Editor Sichtbarkeiten
                            #self.direct_convert_process_layer(layer, external_name, editor_visibility)
                            self.process_layer_v2(layer, tablename, external_name, editor_visibility, joins)
                        else:
                            print("Sichtbarkeit zu " + tablename + " nicht gefunden.")
            self.show_message("Info", "Konvertierung abgeschlossen.")
        else:
            self.show_message("Abbruch", "Abbruch durch Benutzer")

    def process_layer_v2(self, layer, tablename, external_name, editor_visibility, joins):
        layer.setName(external_name)
        # go through all columns of the layer
        for field in layer.fields().toList():
            alias = None
            vis = self.get_vis_setting(editor_visibility, field.name())
            if vis:
                alias = vis.external_fieldname
            join_alias = self.get_join_alias_setting(joins, tablename, field.name())
            if join_alias:
                alias = join_alias
            if alias:
                layer.setFieldAlias(self.get_fieldindex(layer,field), alias)
            # set Editor Type, default: hidden
            setup = QgsEditorWidgetSetup('Hidden', {})
            if alias:
                setup = QgsEditorWidgetSetup('RelationReference',
                                             {
                'AllowAddFeatures':'false',
                'AllowNULL':'false',
                'MapIdentification':'false',
                'OrderByValue':'false',
                'ReadOnly':'false',
                'Relation': self.get_relation(layer, alias),
                'ShowForm':'false',
                'ShowOpenFormButton':'true'}
                )
            if vis:
                if vis.field_type == "date":
                    setup = QgsEditorWidgetSetup('DateTime', {'calendar_popup': '1',
                                                          'display_format': 'dd.MM.yyyy',
                                                          'field_format': 'dd.MM.yyyy',
                                                          'allow_null': '1'})
                elif vis.field_type == "enum":
                    setup = QgsEditorWidgetSetup('ValueMap')
                    # Todo set enum values.
                elif vis.field_type == " boolean":
                    setup = QgsEditorWidgetSetup('CheckBox')
                else:
                    setup = QgsEditorWidgetSetup('TextEdit', {'IsMultiline': 'False'})
            layer.setEditorWidgetSetup(self.get_fieldindex(layer,field), setup)

    def get_relation(self, layer, alias):
        # TODO determine correct relation id
        return "g_anschlussltg_abschnitt_8fb0e60f_8ecb_4cfc_b58d_b15363116904_to_g_hausanschluss_position_hausanschluss_in_betri_ca803d21_f3c7_418f_81d8_02963cfe4c1e"

    def get_fieldindex(self, layer, field):
        return layer.fields().indexFromName(field.name())

    def get_vis_setting(self, editor_visibility, name):
        for vis in editor_visibility:
            if vis.internal_fieldname == name:
                return vis
        return None

    def get_join_alias_setting(self, joins, tablename, name):
        for join in joins:
            if join.own_table == tablename:
                if join.own_field == name:
                    return join.external_name
        return None

    def direct_convert_process_layer(self, layer, external_name, editor_visibility):

        # operation Text
        operation = []

        # get all field names from layer
        layer_field_names = {}
        for layer_field_name in layer.fields():
            layer_field_names[layer_field_name.name()] = layer_field_name

        schemaname, tablename = self.source_table_name(layer)

        doc = QDomDocument()
        map_layer = doc.createElement("maplayer")
        # write active layer xml
        layer.writeLayerXml(map_layer, doc, QgsReadWriteContext())
        layout = map_layer.firstChildElement("editorlayout")

        # set layername to QGIS
        layername_tag = map_layer.firstChildElement("layername")
        layername_tag.firstChild().setNodeValue(external_name)
        #####

        # remove old attributeEditorForm Element if exists
        if map_layer.firstChildElement("datasource").nextSibling().nodeName() == "shortname":
            map_layer.removeChild(map_layer.firstChildElement("shortname").nextSibling())

        datasource = map_layer.firstChildElement("datasource")
        # shortname neu anlegen und positionieren
        newShortNameForm = doc.createElement("shortname")
        newShortNameForm.setNodeValue(tablename)

        map_layer.insertAfter(newShortNameForm, datasource)

        newAttributeEditorForm = doc.createElement("attributeEditorForm")

        # remove old attributeEditorForm Element if exists
        if map_layer.firstChildElement("editorlayout").nextSibling().nodeName() == "attributeEditorForm":
            map_layer.removeChild(map_layer.firstChildElement("editorlayout").nextSibling())

        map_layer.insertAfter(newAttributeEditorForm, layout)
        layout.firstChild().setNodeValue("tablayout")

        store_page_name = "main_page"

        for vis in editor_visibility:

            operation = []
            idx = None
            if vis.internal_fieldname in layer_field_names:

                visibility_values = {"internal_fieldname": vis.internal_fieldname, "page_name": vis.page_name,
                                     "external_page_name": vis.external_page_name, "external_fieldname": vis.external_fieldname,
                                     "field_type": vis.field_type, "enum_name": vis.enum_name}
                print( visibility_values)
                # get fieldIndexNumber from QGIS field
                idx = layer.dataProvider().fieldNameIndex(layer_field_names[vis.internal_fieldname].name())

                if vis.field_type == "date" or vis.internal_fieldname in self.not_changeable_fields():

                    edittypes_tag = map_layer.firstChildElement("edittypes")
                    # get childs editytype from edittypes Tag
                    edittypes_nodes = edittypes_tag.childNodes()

                    for i in range(0, edittypes_nodes.size()):
                        # nodes.at(i).toElement().text() # Inhalt
                        edittype_tag = edittypes_nodes.at(i).toElement()
                        name_value = edittype_tag.attribute("name")  # get value from attr name

                        if vis.internal_fieldname == name_value:

                            # delete child widgetv2config from edittype tag
                            edittype_tag.removeChild(
                                edittypes_nodes.at(i).toElement().firstChildElement("widgetv2config"))

                            # make a new children widgetv2config Tag for parent edittype
                            newWidgetV2Config = doc.createElement("widgetv2config")

                            if vis.field_type == "date":
                                # set new value to attribute widgetv2type
                                edittype_tag.setAttribute("widgetv2type", "DateTime")

                                newWidgetV2Config.setAttribute("calendar_popup", "1")
                                newWidgetV2Config.setAttribute("display_format", "dd.MM.yyyy")
                                newWidgetV2Config.setAttribute("field_format", "dd.MM.yyyy")
                                newWidgetV2Config.setAttribute('allow_null', '1')  # erlaubt Leerwerte
                            if vis.internal_fieldname in self.not_changeable_fields():
                                newWidgetV2Config.setAttribute("fieldEditable",
                                                               "0")  # Feld nicht änderbar

                            edittype_tag.appendChild(newWidgetV2Config)

                # Enumerator Felder und Werte setzen
                if vis.enum_name is not None:

                    enum_values = self.connector.get_enum_values(vis.enum_name,schemaname)

                    edittypes_tag = map_layer.firstChildElement("edittypes")
                    # get childs editytype from edittypes Tag
                    edittypes_nodes = edittypes_tag.childNodes()

                    for i in range(0, edittypes_nodes.size()):

                        # nodes.at(i).toElement().text() # Inhalt
                        edittype_tag = edittypes_nodes.at(i).toElement()
                        name_value = edittype_tag.attribute("name")  # get value from attr name

                        if vis.internal_fieldname == name_value:

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
                            newWidgetV2Config.setAttribute("enum_name", vis.enum_name)

                            edittype_tag.appendChild(newWidgetV2Config)

                            # sets each enumerator value as new value tag
                            for row in enum_values:
                                value = row[0]
                                sequence_number = row[1]
                                newValue = doc.createElement("value")
                                newValue.setAttribute("key", value)
                                newValue.setAttribute("value", value)
                                # set enum name to identify for later
                                newValue.setAttribute("enum_name", vis.enum_name)
                                newWidgetV2Config.appendChild(newValue)

                ## Formulare generieren
                if vis.page_name == "main_page":
                    # alleinstehendes Attribut
                    newEditorField = doc.createElement("attributeEditorField")
                    newEditorField.setAttribute("showLabel", "1")
                    newEditorField.setAttribute("index", str(idx))
                    newEditorField.setAttribute("name", vis.internal_fieldname)
                    newAttributeEditorForm.appendChild(newEditorField)
                else:
                    # set new TabBox
                    if vis.page_name != store_page_name:
                        # Tabbox
                        newEditorContainer = doc.createElement("attributeEditorContainer")
                        newEditorContainer.setAttribute("showLabel", "1")
                        newEditorContainer.setAttribute("visibilityExpressionEnabled", "0")
                        newEditorContainer.setAttribute("visibilityExpression", "")
                        newEditorContainer.setAttribute("name", vis.external_page_name)
                        newEditorContainer.setAttribute("groupBox", "0")
                        newEditorContainer.setAttribute("columnCount", "1")
                        newAttributeEditorForm.appendChild(newEditorContainer)
                    newEditorField = doc.createElement("attributeEditorField")
                    newEditorField.setAttribute("showLabel", "1")
                    newEditorField.setAttribute("index", str(idx))
                    newEditorField.setAttribute("name", vis.internal_fieldname)

                    newEditorContainer.appendChild(newEditorField)

                store_page_name = vis.page_name

            ## set aliases Names for attributes
            if idx is not None:
                map_layer = self.write_aliases_tags(idx, vis, map_layer, doc)

            #### AUSAGBE MELDUNGSFENSTER
        operation.append("Layer " + tablename + " wird bearbeitet:")
        operation.append(".......OK")
        self.dlg.OperationStatments.addItems(operation)
        #### AUSGABE

        # write new DomElement to current active layer
        layer.readLayerXml(map_layer,QgsReadWriteContext())

    def write_aliases_tags(self, idx, visibility, map_layer, doc):

        aliases_tag = map_layer.firstChildElement("aliases")

        # get children from aliases Tag
        nodes = aliases_tag.childNodes()

        for i in range(0, nodes.size()):
            # nodes.at(i).toElement().text() # Inhalt
            alias = nodes.at(i).toElement()
            field_value = alias.attribute("field")

            if visibility.internal_fieldname == field_value:
                my_node = nodes.at(i)

                FieldAttributes = {"field": field_value, "index": str(idx),
                                   "name": visibility.external_fieldname}
                #  QDomDocument / actual node / parent tag / new Subelement Name / Attributes Subelement / remove actual node
                self.create_new_element_tag(doc, my_node, aliases_tag, "alias", FieldAttributes, "true")
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
        return layers

    def get_layer_with_prefix(self, tablename):
        layers = self.read_layers()
        for layer in layers:
            if layer.name().startswith(tablename):
                return layer
        return None

    def create_relations(self, layer, joins, relations):
        for join in joins:
            foreign_layer = self.get_layer_with_prefix(join.foreign_table)
            if foreign_layer:
                relations.append(self.create_1toN_relation(layer, foreign_layer, join.own_field, join.foreign_field))
        return relations

    def create_1toN_relation(self, from_layer, to_layer, from_col, to_col):
        rel = QgsRelation()
        rel.setReferencingLayer(from_layer.id())
        rel.setReferencedLayer(to_layer.id())
        if (from_col in from_layer.dataProvider().fieldNameMap()) and (to_col in to_layer.dataProvider().fieldNameMap()):
            rel.addFieldPair(from_col, to_col)
        else:
            print("create Relations: invalid column name " + from_col + " or " + to_col)
            return None
        rel.setId(from_layer.id() + "_to_" + to_layer.id())
        rel.setName(from_layer.name() + " to " + to_layer.name())
        return rel

    def get_smallworld_page_visibilities(self, project_layers):
        #
        # get editor page visibility from table gced_editorpagefield
        print("Load Smallworld PageVisibility for a set of layers")

        editor_visibility_layers = {}
        for layer in project_layers:
            schemaname, tablename = self.source_table_name(layer)
            editor_visibility_layers[tablename] = self.connector.get_visibilities_from_db(tablename, schemaname)
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
