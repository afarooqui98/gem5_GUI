from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *
import sys

class instantiateDialog(QDialog):
    def __init__(self):
        super(instantiateDialog, self).__init__()

        self.setWindowTitle("Entering Instantiate Mode")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.text = QLabel(self)
        self.text.setText("Warning: Once you instantiate, you cannot modify any values. As such, we will save before continuing.")

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class saveChangesDialog(QDialog):
    def __init__(self, reason):
        super(saveChangesDialog, self).__init__()

        self.setWindowTitle("Save Changes")
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.text = QLabel(self)
        self.text.setText("Would you like to save changes before " + reason + "?")

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
