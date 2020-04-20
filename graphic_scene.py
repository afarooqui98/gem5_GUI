
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from lineDrawer import *
from PySide2.QtCore import *
from gui_views import state
from sym_object import *
import string
import random
import collections
import copy

def convert(data):
    """convert a dictionary with unicode keys and values to utf-8"""

    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

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

    def loadSavedObject(self, type, name, newObject):
        """load object from saved UI file"""
        x = newObject["x"]
        y = newObject["y"]
        z = newObject["z"]
        width = newObject["width"]
        height = newObject["height"]
        component_name = newObject["component_name"]
        parameters = newObject["parameters"]
        connected_objects = newObject["connected_objects"]
        parent = newObject["parent_name"]
        connections = convert(newObject["connections"])

        new_object = SymObject(x, y, width, height, self, component_name, name,
            True, self.state)
        new_object.instance_params = parameters
        new_object.connected_objects = connected_objects
        new_object.parent_name = parent
        new_object.z = z
        new_object.instance_ports = convert(newObject["ports"])

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

        new_object.ui_connections = new_object_connections

        # add new object to backend datastructures
        self.state.sym_objects[name] = new_object
        new_object.initPorts()

        # instantiate the simobject and set its parameters
        new_object.load_instantiate()

        if component_name == "Root":
            #found a root object loaded in from a ui file
            self.state.mainWindow.buttonView.instantiate.setEnabled(True)

        self.addItem(new_object)
        return new_object

    def addObjectToScene(self, type, component_name, name):
        """Creates symobject representation of object and adds to the scene"""
        # generate random string name for object
        if not name:
            name = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(7))

        # add object rectangle to scene
        new_object = SymObject(0, 0, 150, 75, self, component_name, name,
                                False, self.state)

        self.state.sym_objects[name] = new_object

        if component_name == "Root":
            #user created a root object, can instantiate now
            self.state.mainWindow.buttonView.instantiate.setEnabled(True)
        new_object.delete_button.show()
        new_object.rect.setBrush(QColor("Green"))

        self.addItem(new_object)
        return new_object

    def dragEnterEvent(self,event):
        """if an object is dragged into the scene"""
        if self.state.drag_state:
            event.accept()

    def dragMoveEvent(self,event):
        """if an object is dragged around on the scene"""
        if self.state.drag_state:
            event.accept()

    def dropEvent(self,event):
        """if an object is dropped on the scene"""
        if self.state.drag_state:
            event.accept()
        else:
            return
