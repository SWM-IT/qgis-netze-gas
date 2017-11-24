# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeogigPackageCreator
                                 A QGIS plugin
 Plugin to create a package out of geogig manages data etc.
                             -------------------
        begin                : 2017-11-16
        copyright            : (C) 2017 by Markus Heße/Mettenmeier GmbH
        email                : markus.hesse@mettenmeier.de
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
    """Load GeogigPackageCreator class from file GeogigPackageCreator.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .geogig_package_creator import GeogigPackageCreator
    return GeogigPackageCreator(iface)
