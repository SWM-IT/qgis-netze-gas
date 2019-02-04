# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EditorParser
                                 A QGIS plugin
 EditorParser
                              -------------------
        begin                : 2017-09-14
        git sha              : $Format:%H$
        copyright            : (C) 2017-2019 by Thomas Starke and Sebastian Schmidt
        email                : thomas.starke@mettenmeier.de, schmidt.sebastian2@swm.de
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
from typing import Tuple, Iterable, Any, Dict

from PyQt5.QtCore import QTranslator, qVersion, QCoreApplication, QFileInfo
from PyQt5.QtWidgets import QMessageBox, QAction, QFileDialog
from PyQt5.QtGui import *
from PyQt5 import QtGui

from qgis.core import *
from qgis.gui import *


# Initialize Qt resources from file resources.py
# import resources

# Import the code for the dialog
from Join import Join
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
        locale = QtCore.QSettings().value("locale/userLocale")[0:2]
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

    def source_table_name(self, layer: QgsVectorLayer) -> Tuple[str, str]:
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
                            self.build_editor(layer, tablename, external_name, editor_visibility, joins)
                        else:
                            print("Sichtbarkeit zu " + tablename + " nicht gefunden.")
            self.show_message("Info", "Konvertierung abgeschlossen.")
        else:
            self.show_message("Abbruch", "Abbruch durch Benutzer")

    def build_editor(self, layer: QgsVectorLayer, tablename: str, external_name: str, editor_visibility, joins: Iterable[Join]):
        operation = []
        layer.setName(external_name)
        #TODO will this work in all cases?
        layer.setDisplayExpression('system_id')
        # go through all columns of the layer and set correct aliases
        for field in layer.fields().toList():
            alias = None
            vis = self.get_vis_setting(editor_visibility, field.name())
            if vis:
                alias = vis.external_fieldname
            join_alias = self.get_join_alias_setting(joins, tablename, field.name())
            if join_alias:
                alias = join_alias
            if alias:
                layer.setFieldAlias(self.get_fieldindex(layer,field.name()), alias)
            setup = None
            if join_alias:
                relation_id = self.get_relation(layer, field)
                # TODO set the value displayed here
                # seems to be directly Coupbled with layer.setDisplayExpression() (potentially a bug)
                # where to get from?
                # yet unknown
                # how to set Expression?
                # See https://github.com/qgis/QGIS/blob/master/tests/src/python/test_qgsfieldformatters.py
                # QgsRelationReferenceFieldFormatter
                if relation_id:
                    setup = QgsEditorWidgetSetup('RelationReference',
                        {'AllowAddFeatures':'false',
                        'AllowNULL':'false',
                        'MapIdentification':'true',
                        'OrderByValue':'false',
                        'ReadOnly':'false',
                        'Relation': relation_id,
                        'ShowForm':'false',
                        'ShowOpenFormButton':'true'}
                )
            if vis:
                if vis.field_type == "date":
                    setup = QgsEditorWidgetSetup('DateTime', {'calendar_popup': '1',
                                                          'display_format': 'dd.MM.yyyy',
                                                          'field_format': 'dd.MM.yyyy',
                                                          'allow_null': '1'})
                elif (vis.field_type == "string") and vis.enum_name is not None:
                    schema, _ = self.source_table_name(layer)
                    enums = self.connector.get_enum_values(vis.enum_name, schema)
                    entries = []
                    for enum in enums:
                        entries.append({enum[0]:enum[0]})
                    setup = QgsEditorWidgetSetup('ValueMap', {'map': entries})
                elif vis.field_type == "boolean":
                    setup = QgsEditorWidgetSetup('CheckBox', {})
                else:
                    setup = QgsEditorWidgetSetup('TextEdit', {'IsMultiline': 'False'})
            if setup:
                layer.setEditorWidgetSetup(self.get_fieldindex(layer, field.name()), setup)

        # Configure Field editors in correct order
        form_config = layer.editFormConfig()
        form_config.setLayout(QgsEditFormConfig.EditorLayout.TabLayout)
        form_config.invisibleRootContainer().clear()
        root_container = form_config.invisibleRootContainer()
        current_container = form_config.invisibleRootContainer()
        current_pagename = "main_page"
        for vis in editor_visibility:
            if vis.page_name != current_pagename:
                new_container = self.create_tab_box(root_container, vis.external_page_name)
                form_config.addTab(new_container)
                current_container = new_container
                current_pagename = vis.page_name
            fieldname = vis.internal_fieldname
            if vis.field_type == 'geometry':
                continue
            if vis.field_type == 'join':
                join_target_field_name = self.get_join_target_field(joins, vis.external_fieldname)
                if join_target_field_name:
                    fieldname = join_target_field_name
                else:
                    continue
            editor_field = QgsAttributeEditorField(fieldname, self.get_fieldindex(layer, fieldname), current_container)
            current_container.addChildElement(editor_field)
        layer.setEditFormConfig(form_config)

        operation.append("Layer " + tablename + " wird bearbeitet:")
        operation.append(".......OK")
        self.dlg.OperationStatments.addItems(operation)

    def create_tab_box(self, parent, name:str) -> QgsAttributeEditorContainer:
        container = QgsAttributeEditorContainer(name, parent)
        container.setIsGroupBox(False)
        container.setColumnCount(1)
        return container

    def get_relation(self, layer : QgsVectorLayer, field) -> QgsRelation:
        relations = QgsProject.instance().relationManager().referencingRelations(layer)
        if relations:
            for relation in relations:
                fields_indices = relation.referencingFields()
                for field_index in fields_indices:
                    if self.get_fieldindex(layer,field.name()) == field_index:
                        return relation.id()
        return None

    def get_fieldindex(self, layer: QgsVectorLayer, name: str) -> int:
        return layer.fields().indexFromName(name)

    def get_vis_setting(self, editor_visibility, name: str):
        for vis in editor_visibility:
            if vis.internal_fieldname == name:
                return vis
        return None

    def get_join_alias_setting(self, joins: Iterable[Join], tablename: str, name: str) -> str:
        for join in joins:
            if join.own_table == tablename:
                if join.own_field == name:
                    return join.external_name
        return None

    def get_join_target_field(self, joins: Iterable[Join], external_name:str) -> str:
        for join in joins:
            if join.external_name == external_name:
                return join.own_field
        return None

    def read_layers(self) -> Iterable[QgsVectorLayer]:
        # read my project Layers from project
        layers = [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()]
        return layers

    def get_layer_with_prefix(self, tablename:str) -> QgsVectorLayer:
        layers = self.read_layers()
        for layer in layers:
            if layer.name().startswith(tablename):
                return layer
        return None

    def create_relations(self, layer: QgsVectorLayer, joins : Iterable[Join], relations):
        for join in joins:
            foreign_layer = self.get_layer_with_prefix(join.foreign_table)
            if foreign_layer:
                relations.append(self.create_1toN_relation(layer, foreign_layer, join.own_field, join.foreign_field))
        return relations

    def create_1toN_relation(self, from_layer:str, to_layer:str, from_col:str, to_col:str) -> QgsRelation:
        rel = QgsRelation()
        rel.setReferencingLayer(from_layer.id())
        rel.setReferencedLayer(to_layer.id())
        if (from_col in from_layer.dataProvider().fieldNameMap()) and (to_col in to_layer.dataProvider().fieldNameMap()):
            rel.addFieldPair(from_col, to_col)
        else:
            print("create Relations: invalid column name " + from_col + " or " + to_col)
            return None
        _, table1 = self.source_table_name(from_layer)
        _, table2 = self.source_table_name(to_layer)
        rel.setId(table1 + "_to_" + table2)
        rel.setName(from_layer.name() + " to " + to_layer.name())
        return rel

    def get_smallworld_page_visibilities(self, project_layers: Iterable[QgsVectorLayer]) -> Dict[str,Any]:
        editor_visibility_layers = {}
        for layer in project_layers:
            schemaname, tablename = self.source_table_name(layer)
            editor_visibility_layers[tablename] = self.connector.get_visibilities_from_db(tablename, schemaname)
        return editor_visibility_layers

    def show_message(self, title: str, text: str):
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
