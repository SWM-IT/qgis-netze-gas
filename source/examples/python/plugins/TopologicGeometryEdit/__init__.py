# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TopologicGeometryEdit
                                 A QGIS plugin
 This plugin adds functions to edit topological linked geometries in one step
                             -------------------
        begin                : 2017-09-21
        copyright            : (C) 2017 by H.Fischer/Mettenmeier GmbH
        email                : holger.fischer@mettenmeier.de
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
    """Load TopologicGeometryEdit class from file TopologicGeometryEdit.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .topoGeomEdit import TopologicGeometryEdit
    return TopologicGeometryEdit(iface)
