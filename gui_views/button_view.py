from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *

import sys, random
import copy
import config
from button import *
import json

class ButtonView(): #export, draw line, save and load configuration buttons
    def __init__(self, layout):
        self.wireButton = QPushButton("draw wire")
        layout.addWidget(self.wireButton)
        self.exportButton = QPushButton("export")
        layout.addWidget(self.exportButton)
        self.saveUIButton = QPushButton("Save Configuration")
        layout.addWidget(self.saveUIButton)
        self.openUIButton = QPushButton("Open Configuration")
        layout.addWidget(self.openUIButton)

        self.wireButton.clicked.connect(wire_button_pressed)
        self.exportButton.clicked.connect(export_button_pressed)
        self.saveUIButton.clicked.connect(saveUI_button_pressed)
        self.openUIButton.clicked.connect(openUI_button_pressed)
