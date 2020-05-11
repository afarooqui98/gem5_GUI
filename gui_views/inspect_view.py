from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *
from m5_calls import *

import sys, random
import copy
from gui_views import state
import json
import logging

class InspectWidget(QWidget):
    def __init__(self, state):
        super(InspectWidget, self).__init__()
        self.state = state
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

    def populate(self, isObject, attributeList):
        if isObject:
            print("is object")
        else:
            print("is wire")

        for attr in attributeList:
            label = QLabel()
            label.setText(attr)
            label.setStyleSheet("qproperty-alignment: AlignJustify;")
            self.layout.addWidget(label)

    def clear(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
