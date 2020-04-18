from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *
from m5_calls import *

import sys, random
import copy
from gui_views import state
import json

class DebugWidget(QWidget):
    """ Displays options for development and allows enabling of these options"""
    def __init__(self, state):
        super(DebugWidget, self).__init__()
        self.state = state

        self.debug_layout = QVBoxLayout()
        btn_1 = QPushButton('1')
        btn_2 = QPushButton('2')
        btn_3 = QPushButton('3')
        btn_4 = QPushButton('4')

        #search bar
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Search for a debug flag here!")
        self.edit.setFixedWidth(250)


        self.debug_layout.addWidget(btn_1)
        self.debug_layout.addWidget(btn_2)
        self.debug_layout.addWidget(btn_3)
        self.debug_layout.addWidget(btn_4)
        self.debug_layout.addWidget(self.edit)

        self.debug_layout.addStretch(5)
        self.debug_layout.setSpacing(10)

        self.setLayout(self.debug_layout)
