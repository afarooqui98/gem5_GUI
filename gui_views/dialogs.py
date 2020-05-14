from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *
import sys

class instantiateDialog(QDialog):
    def __init__(self, state):
        super(instantiateDialog, self).__init__(state.mainWindow.main)

        self.setWindowTitle("Entering Instantiate Mode")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.text = QLabel(self)
        self.text.setText("""Warning: Once you instantiate, you cannot modify
any values. As such, we will save before continuing.""")

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class saveChangesDialog(QDialog):
    def __init__(self, reason, state):
        super(saveChangesDialog, self).__init__(state.mainWindow.main)

        self.setWindowTitle("Save Changes")
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.text = QLabel(self)
        self.text.setText("Would you like to save before " + reason + "?")

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class deleteWireDialog(QDialog):
    def __init__(self, dialogText):
        super(deleteWireDialog, self).__init__()

        self.setWindowTitle("Deleting wire")
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.text = QLabel(self)
        self.text.setText(dialogText)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class errorDialog(QDialog):
    def __init__(self, state, msg):
        super(errorDialog, self).__init__(state.mainWindow.main)

        self.setWindowTitle("FATAL ERROR")
        QBtn = QDialogButtonBox.Ok

        self.text = QLabel(self)
        self.text.setText(msg)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class addChildDialog(QDialog):
    def __init__(self, dialogText):
        super(addChildDialog, self).__init__()

        self.setWindowTitle("Add new child")
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.text = QLabel(self)
        self.text.setText(dialogText)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
