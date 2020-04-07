from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *

import sys, random
import copy
from gui_views import state
import json

class AttributeView(): #table view for parameters, as well as the description
    def __init__(self, layout, state):
        self.state = state
        #attribute table for an object, is editable
        self.attributeLayout = QHBoxLayout()
        self.attributeTable = QTableWidget(0,2)
        self.attributeTable.setObjectName("attributeTable")
        self.attributeTable.verticalHeader().setVisible(False)
        self.attributeTable.horizontalHeader().setVisible(False)
        header = self.attributeTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.attributeLayout.addWidget(self.attributeTable)

        layout.addLayout(self.attributeLayout)

        #description label
        self.label = QLabel()
        self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setScaledContents(True)
        layout.addWidget(self.label)

        #handlers
        self.attributeTable.itemDoubleClicked.connect(self.makeEditable)

    # this function feeds into the next one, after the cell is changed it will
    # trigger
    def makeEditable(self, item):
        # set item to editable
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.attributeTable.itemChanged.connect(self.modifyFields)

    # this signal disconnects itself after finishing execution, since we only
    # want to trigger it AFTER a double press
    def modifyFields(self, item):
        if self.state.current_sym_object == None or not item:
            return

        # get attributes
        currentColumn = self.attributeTable.column(item)
        currentRow = self.attributeTable.row(item)
        currentAttribute = self.attributeTable.item(currentRow,
                                                    currentColumn - 1).text()
        currentValue = item.text()

        # if the value is name or connected objects, set the param instead of
        # the dict
        if currentAttribute == "Name":
            self.state.current_sym_object.updateName(currentValue)
            current_x = self.state.current_sym_object.x
            current_y = self.state.current_sym_object.y
            current_name = self.state.current_sym_object.name
            
            self.state.sym_objects[current_name] = self.state.current_sym_object
        elif currentAttribute == "Child Objects":
            self.state.current_sym_object.connected_objects = currentValue
            self.state.sym_objects[currentValue].to_export = 0
            self.state.line_drawer.connectSubObject(self.state.current_sym_object.name,
                                                currentValue)
        else:
            if currentAttribute not in self.state.current_sym_object.parameters:
                self.state.current_sym_object.parameters[currentAttribute] = {}
                if "Value" not in self.state.current_sym_object.parameters[currentAttribute]:
                    self.state.current_sym_object.parameters[currentAttribute]["Value"] = currentValue
                    self.state.current_sym_object.parameters[currentAttribute]["Type"] = \
                        self.state.catalog["SimObject"][self.state.current_sym_object.component_name]['ports'][currentAttribute]['Type']
            else:
                self.state.current_sym_object.parameters[currentAttribute]["Value"] = \
                                                                    currentValue

        # item no longer editable, disconnect
        self.attributeTable.itemChanged.disconnect(self.modifyFields)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        if currentValue:
            item.setBackground(QColor("white"))
