from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *

import sys, random
import copy
from gui_views import state
import json

class ButtonView(): #export, draw line, save and load self.stateuration buttons
    def __init__(self, layout, state):
        self.state = state
        # create buttons and add to layout
        self.wireButton = QPushButton("draw wire")
        layout.addWidget(self.wireButton)
        self.exportButton = QPushButton("export")
        layout.addWidget(self.exportButton)
        self.saveUIButton = QPushButton("Save Configuration")
        layout.addWidget(self.saveUIButton)
        self.openUIButton = QPushButton("Open Configuration")
        layout.addWidget(self.openUIButton)

        # connect each button to its event handler
        self.wireButton.clicked.connect(self.wire_button_pressed)
        self.exportButton.clicked.connect(self.export_button_pressed)
        self.saveUIButton.clicked.connect(self.saveUI_button_pressed)
        self.openUIButton.clicked.connect(self.openUI_button_pressed)

    # changes gui state to allow for wire drawing and disable object dragging
    def wire_button_pressed(self):
        self.state.drag_state = not self.state.drag_state
        self.state.draw_wire_state = not self.state.draw_wire_state
        self.state.setDragState()


    # creates a python file that can be run with gem5
    def export_button_pressed(self):
        for object in self.state.sym_objects.values():
            print(object.component_name)

    # loads .ui file into gui
    def openUI_button_pressed(self):

        # show dialog box for user to select a file to open
        filename = QFileDialog.getOpenFileName(None, 'Open file',
       '',"gem5 UI Files (*.ui)")[0]

       # stop if cancel is pressed or there is an error
        if not filename:
            return

        #clear out existing objects before loading from file
        for object in self.state.sym_objects.values():
            self.state.scene.removeItem(object)

        self.state.sym_objects.clear()
        self.state.coord_map.clear()

        # read data in from the file and load each object
        with open(filename) as json_file:
            data = json.load(json_file)
            for key in data:
                object = data[key]
                self.state.scene.loadSavedObject("component", key, object)

    # saves gui state to a .ui file
    def saveUI_button_pressed(self):
        savedObjects = {}

        # iterate through the current objects on the scene and create a new JSON
        # object for each one
        for object in self.state.sym_objects.values():
            newObject = {}
            newObject["x"] = object.x
            newObject["y"] = object.y
            newObject["z"] = object.z
            newObject["width"] = object.width
            newObject["height"] = object.height
            newObject["component_name"] = object.component_name
            newObject["name"] = object.name
            newObject["parent_name"] = object.parent_name

            newObject["parameters"] = object.parameters
            newObject["connected_objects"] = object.connected_objects
            newObject["connections"] = object.connections
            savedObjects[object.name] = newObject

        # show dialog box to let user create output file
        filename = QFileDialog.getSaveFileName(None, "",
                                           "",
                                           "gem5 UI Files (*.ui)")[0]
        # stop if cancel is pressed
        if not filename:
            return

        # with the selected file write our JSON object
        with open(filename, 'w') as outfile:
            json.dump(savedObjects, outfile)
