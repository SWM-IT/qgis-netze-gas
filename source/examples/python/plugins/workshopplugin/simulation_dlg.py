import os

from PyQt4 import QtGui,uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'simulation_dlg.ui'))
	
class simulationDialog(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, parent=None):
        """Constructor."""
        super(simulationDialog, self).__init__(parent)
        self.setupUi(self)
