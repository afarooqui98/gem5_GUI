
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from lineDrawer import *
from PySide2 import QtCore
from gui_views import state
from sym_object import *
import string
import random

class GraphicsScene(QGraphicsScene):
    """this class provides a scene to manage objects"""

    # constructor
    def __init__(self, x, y, width, height, state):
        super(GraphicsScene, self).__init__(x, y, width, height)
        self.state = state
        self.state.line_drawer = LineDrawer(state)
        self.state.line_drawer.resize(self.width(), self.height())
        self.addWidget(self.state.line_drawer)

    # load object from saved UI file
    def loadSavedObject(self, type, name, newObject):

        x = newObject["x"]
        y = newObject["y"]
        z = newObject["z"]
        width = newObject["width"]
        height = newObject["height"]
        component_name = newObject["component_name"]
        parameters = newObject["parameters"]
        connected_objects = newObject["connected_objects"]
        parent = newObject["parent_name"]

        new_object = SymObject(x, y, width, height, self, component_name, name, True, self.state)
        new_object.parameters = parameters
        new_object.connected_objects = connected_objects
        new_object.parent_name = parent
        new_object.z = z

        # add new object to backend datastructures
        self.state.sym_objects[name] = new_object
        self.state.current_sym_object = new_object
        self.addItem(new_object)
        return new_object

    def addObjectToScene(self, type, component_name, name):

        # generate random string name for object
        if not name:
            name = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(7))

        # add object rectangle to scene

        new_object = SymObject(0, 0, 150, 75, self, component_name, name,
                                False, self.state)

        self.state.sym_objects[name] = new_object
        self.state.current_sym_object = new_object
        self.addItem(new_object)
        return new_object

    # if an object is dragged into the scene
    def dragEnterEvent(self,event):
        if self.state.drag_state:
            event.accept()

    # if an object is dragged around on the scene
    def dragMoveEvent(self,event):
        if self.state.drag_state:
            event.accept()

    # if an object is dropped on the scene
    def dropEvent(self,event):
        if self.state.drag_state:
            event.accept()
        else:
            return
