from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphic_scene import *

import sys

class instantiateDialog(QDialog):
    def __init__(self, state):
        # Add dialog in the context of the main window
        super(instantiateDialog, self).__init__(state.mainWindow.main)

        # Configure the dialog with text and options
        self.setWindowTitle("Entering Instantiate Mode")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.text = QLabel(self)
        self.text.setText("""Warning: Once you instantiate, you cannot modify
                            any values. As such, we will save before
                            continuing.""")

        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Create new layout for the dialog box and add text/button widgets to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class saveChangesDialog(QDialog):
    def __init__(self, reason, state):
        # Add dialog in the context of the main window
        super(saveChangesDialog, self).__init__(state.mainWindow.main)

        # Configure the dialog with text and options
        self.setWindowTitle("Save Changes")
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.text = QLabel(self)
        self.text.setText("Would you like to save before " + reason + "?")

        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Create new layout for the dialog box and add text/button widgets to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class deleteWireDialog(QDialog):
    def __init__(self, dialogText):
        super(deleteWireDialog, self).__init__()

        # Configure the dialog with text and options
        self.setWindowTitle("Deleting wire")
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.text = QLabel(self)
        self.text.setText(dialogText)

        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Create new layout for the dialog box and add text/button widgets to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class errorDialog(QDialog):
    def __init__(self, state, msg):
        # Add dialog in the context of the main window
        super(errorDialog, self).__init__(state.mainWindow.main)

        # Configure the dialog with text and options
        self.setWindowTitle("FATAL ERROR")
        QBtn = QDialogButtonBox.Ok

        self.text = QLabel(self)
        self.text.setText(msg)

        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)

        # Create new layout for the dialog box and add text/button widgets to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class addChildDialog(QDialog):
    def __init__(self, dialogText):
        super(addChildDialog, self).__init__()

        # Configure the dialog with text and options
        self.setWindowTitle("Add new child")
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.text = QLabel(self)
        self.text.setText(dialogText)

        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Create new layout for the dialog box and add text/button widgets to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
