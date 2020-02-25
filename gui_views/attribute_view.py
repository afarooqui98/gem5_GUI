from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *

import sys, random
import copy
import config
import json

class AttributeView(): #table view for parameters, as well as the description
    def __init__(self, layout):
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
        if config.current_sym_object == None or not item:
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
            config.current_sym_object.name = currentValue
            current_x = config.current_sym_object.x
            current_y = config.current_sym_object.y
            current_name = config.current_sym_object.name
            if (current_x, current_y) in config.coord_map:
                del config.sym_objects[config.coord_map[(current_x, current_y)]]

            config.coord_map[(current_x, current_y)] = current_name
            config.sym_objects[current_name] = config.current_sym_object
        elif currentAttribute == "Child Objects":
            config.current_sym_object.connected_objects = currentValue
            config.sym_objects[currentValue].to_export = 0
            config.line_drawer.connectSubObject(config.current_sym_object.name,
                                                currentValue)
        else:
            config.current_sym_object.parameters[currentAttribute]["Value"] = \
                                                                    currentValue

        # item no longer editable, disconnect
        self.attributeTable.itemChanged.disconnect(self.modifyFields)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        if currentValue:
            item.setBackground(QColor("white"))
