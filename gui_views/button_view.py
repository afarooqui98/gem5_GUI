from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *
from dialogs import *

import sys, random
import copy
from gui_views import state
import json

from m5_calls import *

class ButtonView(): #export, draw line, save and load self.stateuration buttons
    def __init__(self, layout, state, window):
        self.state = state

        mainMenu = window.menuBar()

        saveAction = QAction("Save", window)
        saveAction.triggered.connect(self.save_button_pressed)
        saveAsAction = QAction("Save As", window)
        saveAsAction.triggered.connect(self.save_as_UI_button_pressed)
        openAction = QAction("Open", window)
        openAction.triggered.connect(self.openUI_button_pressed)

        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(openAction)

        copyAction = QAction("Copy", window)
        copyAction.triggered.connect(self.copy_button_pressed)
        pasteAction = QAction("Paste", window)
        pasteAction.triggered.connect(self.paste_button_pressed)
        undoAction = QAction("Undo", window)
        undoAction.triggered.connect(self.undo_button_pressed)

        editMenu = mainMenu.addMenu('Edit')
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)
        editMenu.addAction(undoAction)

        instantiateAction = QAction("Instantiate", window)
        instantiateAction.triggered.connect(self.export_button_pressed)
        simulateAction = QAction("Simulate", window)
        simulateAction.triggered.connect(self.simulate_button_pressed)

        runMenu = mainMenu.addMenu('Run')
        runMenu.addAction(instantiateAction)
        runMenu.addAction(simulateAction)

        wireAction = QAction("Enable Wire", window)
        wireAction.triggered.connect(self.wire_button_pressed)

        toolsMenu = mainMenu.addMenu('Tools')
        toolsMenu.addAction(wireAction)

    # changes gui state to allow for wire drawing and disable object dragging
    def wire_button_pressed(self):
        self.state.drag_state = not self.state.drag_state
        self.state.draw_wire_state = not self.state.draw_wire_state
        self.state.setDragState()

    #TODO
    def copy_button_pressed(self):
        print("copy button pressed")
        return

    #TODO
    def paste_button_pressed(self):
        print ("paste button pressed")
        return

    #TODO
    def undo_button_pressed(self):
        print ("undo button pressed")
        return

    # creates a python file that can be run with gem5
    def export_button_pressed(self):
        dlg = instantiateDialog()
        if dlg.exec_():
            print("Success!")
            self.save_button_pressed() #want to save before instantiation
            for object in self.state.sym_objects.values():
                if object.component_name == "Root":
                    root_name , root = traverse_hierarchy_root(self.state.sym_objects, object)
                    instantiate() #actual m5 instatiation
                    self.simulateButton.setEnabled(True)
                    self.exportButton.setEnabled(False)
        else:
            print("Cancel!")

    # creates a python file that can be run with gem5
    def simulate_button_pressed(self):
        simulate()

    # loads .ui file into gui
    def openUI_button_pressed(self):
        if self.state.sym_objects:
            dialog = saveChangesDialog("opening a new file")
            if dialog.exec_():
                self.save_button_pressed()
            else:
                print("dont save changes")

        # show dialog box for user to select a file to open
        filename = QFileDialog.getOpenFileName(None, 'Open file',
       '',"gem5 UI Files (*.ui)")[0]

       # stop if cancel is pressed or there is an error
        if not filename:
            return

        self.state.fileName = filename

        # get file name from path
        tokens = filename.split('/')
        self.state.mainWindow.setWindowTitle("gem5 GUI | " + tokens[-1])

        #clear out existing objects before loading from file
        for object in self.state.sym_objects.values():
            for name, connection in object.connections.items():
                if connection.line:
                    self.state.scene.removeItem(connection.line)

            self.state.scene.removeItem(object)
            object.connections.clear()

        self.state.sym_objects.clear()
        self.state.coord_map.clear()

        # read data in from the file and load each object
        with open(filename) as json_file:
            data = json.load(json_file)
            z_score = 0
            while str(z_score) in data:
                cur_z_array = data[str(z_score)]
                for object in cur_z_array:
                    self.state.scene.loadSavedObject("component",
                                                    object["name"], object)

                z_score += 1

            self.state.line_drawer.update()

    def getOutputData(self):
        savedObjects = {}

        # iterate through the current objects on the scene and create a new JSON
        # object for each one
        for object in self.state.sym_objects.values():
            newObject = {}
            newObject["x"] = object.scenePos().x()
            newObject["y"] = object.scenePos().y()
            newObject["z"] = object.z
            newObject["width"] = object.width
            newObject["height"] = object.height
            newObject["component_name"] = object.component_name
            newObject["name"] = object.name
            newObject["parent_name"] = object.parent_name

            params = {}
            #Storing the parameters
            for param in object.parameters:
                params[str(param)] = {}

                # TODO: Insert err message here if a parameter has not been set
                if object.parameters[param]["Value"] is None:
                    print("Error must set required parameter")
                    params[str(param)]["Value"] = None

                #Only need to store the values of parameters changed for now
                if object.parameters[param]["Default"] != \
                    object.parameters[param]["Value"]:
                    param_type = type(object.parameters[param]["Value"])
                    if (param_type == str or param_type == int or \
                            param_type == bool or param_type == unicode or \
                            param_type == list):
                        params[str(param)]["Value"] = \
                            object.parameters[param]["Value"]
                    else:
                        # weird case if a value is a class but shouldn't really
                        #   hit this case since all user inputs are strings
                        params[str(param)]["Value"] = \
                            object.parameters[param]["Value"].__dict__

            newObject["parameters"] = params

            ports = {}
            for port in object.ports.keys():
                ports[port] = {}
                print(type(object.ports[port]["Value"]))
                ports[port]["Value"] = str(object.ports[port]["Value"])

            newObject["ports"] = ports
            newObject["connected_objects"] = object.connected_objects

            connections = []

            for c in object.connections:
                newConnection = {}
                newConnection["key"] = c
                newConnection["parent_endpoint_x"] = \
                        object.connections[c].parent_endpoint.x()
                newConnection["parent_endpoint_y"] = \
                        object.connections[c].parent_endpoint.y()
                newConnection["child_endpoint_x"] = \
                        object.connections[c].child_endpoint.x()
                newConnection["child_endpoint_y"] = \
                        object.connections[c].child_endpoint.y()
                newConnection["parent_port_num"] = \
                        object.connections[c].parent_port_num
                newConnection["child_port_num"] = \
                        object.connections[c].child_port_num
                connections.append(newConnection)

            newObject["connections"] = connections

            if object.z not in savedObjects:
                savedObjects[object.z] = []

            savedObjects[object.z].append(newObject)

        return savedObjects


    def save_button_pressed(self):
        if self.state.fileName:
            filename = self.state.fileName
        else:
            # show dialog box to let user create output file
            filename = QFileDialog.getSaveFileName(None, "",
                                           "",
                                           "gem5 UI Files (*.ui)")[0]
        # stop if cancel is pressed
        if not filename:
            return

        savedObjects = self.getOutputData()

        # with the selected file write our JSON object
        with open(filename, 'w') as outfile:
            json.dump(savedObjects, outfile)

        # get file name from path
        tokens = filename.split('/')
        self.state.mainWindow.setWindowTitle("gem5 GUI | " + tokens[-1])

    # saves gui state to a .ui file
    def save_as_UI_button_pressed(self):

        # show dialog box to let user create output file
        filename = QFileDialog.getSaveFileName(None, "",
                                           "",
                                           "gem5 UI Files (*.ui)")[0]
        # stop if cancel is pressed
        if not filename:
            return

        savedObjects = self.getOutputData()

        # with the selected file write our JSON object
        with open(filename, 'w') as outfile:
            json.dump(savedObjects, outfile)

        # get file name from path
        tokens = filename.split('/')
        self.state.mainWindow.setWindowTitle("gem5 GUI | " + tokens[-1])
