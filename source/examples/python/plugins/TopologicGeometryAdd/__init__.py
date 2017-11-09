# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TopologicGeometryAdd
                                 A QGIS plugin
 add new objects with topo geoms
                             -------------------
        begin                : 2017-10-25
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
    """Load TopologicGeometryAdd class from file TopologicGeometryAdd.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .topoGeomAdd import TopologicGeometryAdd
    return TopologicGeometryAdd(iface)
