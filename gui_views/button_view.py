from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *

import sys, random
import copy
from gui_views import config
import json

class ButtonView(): #export, draw line, save and load configuration buttons
    def __init__(self, layout):
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
        self.wireButton.clicked.connect(wire_button_pressed)
        self.exportButton.clicked.connect(export_button_pressed)
        self.saveUIButton.clicked.connect(saveUI_button_pressed)
        self.openUIButton.clicked.connect(openUI_button_pressed)

# changes gui state to allow for wire drawing and disable object dragging
def wire_button_pressed():
    config.drag_state = not config.drag_state
    config.draw_wire_state = not config.draw_wire_state
    config.setDragState()


# creates a python file that can be run with gem5
def export_button_pressed():
    file = open("run_simple.py", "w+")
    file.write("""# -*- coding: utf-8 -*-
# Copyright (c) 2020 Brownies
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Brownies\n"""
    )

    file.write("""\nfrom __future__ import print_function
from __future__ import absolute_import

# import the m5 (gem5) library created when gem5 is built
import m5
# import all of the SimObjects
from m5.objects import *\n\n"""
    )

    file.write(config.getSymObjects())

    file.write("""\n
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))"""
    )

# loads .ui file into gui
def openUI_button_pressed():

    # show dialog box for user to select a file to open
    filename = QFileDialog.getOpenFileName(None, 'Open file',
   '',"gem5 UI Files (*.ui)")[0]

   # stop if cancel is pressed or there is an error
    if not filename:
        return

    #clear out existing objects before loading from file
    for object in config.sym_objects.values():
        config.scene.removeItem(object)

    config.sym_objects.clear()
    config.coord_map.clear()

    # read data in from the file and load each object
    with open(filename) as json_file:
        data = json.load(json_file)
        for key in data:
            object = data[key]
            config.scene.loadSavedObject("component", key, object)

    for parent in config.sym_objects:
        children = config.sym_objects[parent].connected_objects
        print("parent: ", parent)
        print("children: ", children)
        if children:
            for child in children:
                config.sym_objects[child].resizeUIObject(\
                                                config.sym_objects[parent], 0)


# saves gui state to a .ui file
def saveUI_button_pressed():
    savedObjects = {}

    # iterate through the current objects on the scene and create a new JSON
    # object for each one
    for object in config.sym_objects.values():
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
