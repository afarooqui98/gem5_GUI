
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from lineDrawer import *
from PySide2.QtCore import *
from gui_views import state
from sym_object import *
from m5_calls import load_instantiate
import string
import random
import copy

class GraphicsScene(QGraphicsScene):
    """this class provides a scene to manage objects"""

    # constructor
    def __init__(self, x, y, width, height, state):
        super(GraphicsScene, self).__init__(x, y, width, height)
        self.state = state
        self.state.line_drawer = LineDrawer(state)
        self.state.line_drawer.resize(self.width(), self.height())

        # change background of canvas to light gray
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.lightGray)
        self.state.line_drawer.setAutoFillBackground(True)
        self.state.line_drawer.setPalette(pal)

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
        connections = newObject["connections"]

        new_object = SymObject(x, y, width, height, self, component_name, name,
            True, self.state)
        new_object.parameters = parameters
        new_object.connected_objects = connected_objects
        new_object.parent_name = parent
        new_object.z = z
        new_object.ports = newObject["ports"]

        print("\nports are:")
        print(newObject["ports"])

        new_object_connections = {}

        # rebuild the connection dictionary for the object
        for connection in connections:
            parent_endpoint = QPointF(connection["parent_endpoint_x"],
                                        connection["parent_endpoint_y"])
            child_endpoint = QPointF(connection["child_endpoint_x"],
                                        connection["child_endpoint_y"])
            new_connection = Connection(parent_endpoint, child_endpoint,
                                            connection["parent_port_num"],
                                            connection["child_port_num"])
            key = (connection["key"][0], connection["key"][1],
                connection["key"][2], connection["key"][3])
            new_object_connections[key] = new_connection

        new_object.connections = new_object_connections

        # add new object to backend datastructures
        self.state.sym_objects[name] = new_object
        self.state.current_sym_object = new_object
        self.state.current_sym_object.SimObject = \
            copy.deepcopy(
        self.state.instances[self.state.current_sym_object.component_name])
        self.state.current_sym_object.initPorts()

        # instantiate the simobject and set its parameters
        load_instantiate(self.state.current_sym_object)

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

        #self.state.current_sym_object = new_object
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
