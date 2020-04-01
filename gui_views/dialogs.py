from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys

class instantiateDialog(QDialog):
    def __init__(self):
        super(instantiateDialog, self).__init__()

        self.setWindowTitle("Entering Instantiate Mode")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
