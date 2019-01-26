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
    import os

    debug_flag = os.environ.get('PY_DEBUG_FLAG', '')
    debug_egg = os.environ.get('PY_DEBUG_EGG', '')
    debug_port = os.environ.get('PY_DEBUG_PORT', '')

    if debug_flag:
        sys.path.append(debug_egg)
        import pydevd
        #TODO use debug_port
        pydevd.settrace('localhost', port=42424, stdoutToServer=True, stderrToServer=True)
    from .editorparser import EditorParser
    return EditorParser(iface)
