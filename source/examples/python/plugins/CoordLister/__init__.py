# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoordLister
                                 A QGIS plugin
 List Coordinates
                             -------------------
        begin                : 2017-09-11
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
    """Load CoordLister class from file CoordLister.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .coord_lister import CoordLister
    return CoordLister(iface)
