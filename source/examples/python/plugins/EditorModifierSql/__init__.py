# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EditorModifierSql
                                 A QGIS plugin
 Editor modifier SQL
                             -------------------
        begin                : 2017-09-12
        copyright            : (C) 2017 by Thomas Starke
        email                : thomas.starke@mettenmeier.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load EditorModifierSql class from file EditorModifierSql.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .editor_modifier import EditorModifierSql
    return EditorModifierSql(iface)
