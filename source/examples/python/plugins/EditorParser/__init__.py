# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EditorParser
                                 A QGIS plugin
 EditorParser
                             -------------------
        begin                : 2017-09-14
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
    """Load EditorParser class from file EditorParser.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    import sys
    # TODO determine if we're in a Debug Environemnt and pull path from an  environment variable
    sys.path.append('C:\Program Files\JetBrains\PyCharm 2018.3.3\debug-eggs\pycharm-debug.egg')
    import pydevd
    pydevd.settrace('localhost', port=42424, stdoutToServer=True, stderrToServer=True)
    from .editorparser import EditorParser
    return EditorParser(iface)
