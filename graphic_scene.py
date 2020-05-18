import collections
import copy
import random
import string

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from gui_views import state
from lineDrawer import *
from sym_object import *

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
        self.default_width = width
        self.default_height = height
        self.state.line_drawer = LineDrawer(state)
        self.setLineDrawer()
        self.addWidget(self.state.line_drawer)

    def loadSymObject(self, name, new_object):
        """Creates the sym object from the necessary UI fields"""
        x = new_object["x"]
        y = new_object["y"]
        width = new_object["width"]
        height = new_object["height"]
        component_name = convert(new_object["component_name"])
        if component_name == "Root":
            #found a root object loaded in from a ui file
            self.state.mainWindow.buttonView.instantiate.setEnabled(True)

        return SymObject(x, y, width, height, self, component_name, name,
            True, self.state)

    def setSymObjectFields(self, sym_object, new_object):
        """Sets backend fields for the sym object"""
        sym_object.instance_params = new_object["parameters"]
        sym_object.connected_objects = new_object["connected_objects"]
        sym_object.parent_name = new_object["parent_name"]
        sym_object.z = new_object["z"]
        sym_object.instance_ports = convert(new_object["ports"])

    def setSymObjectConnections(self, sym_object, new_object):
        """Builds the connection dictionary for the sym object"""
        connections = convert(new_object["connections"])
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

        sym_object.ui_connections = new_object_connections


    def loadSavedObject(self, type, name, new_object):
        """load object from saved UI file"""
        sym_object = self.loadSymObject(name, new_object)
        self.setSymObjectFields(sym_object, new_object)
        self.setSymObjectConnections(sym_object, new_object)
        sym_object.initPorts()
        # instantiate the simobject and set its parameters
        sym_object.load_instantiate()

        # add new object to backend datastructures
        self.state.sym_objects[name] = sym_object

        self.state.highlightIncomplete()
        self.addItem(sym_object)
        return sym_object


    def addObjectToScene(self, type, component_name, name):
        """Creates symobject representation of object and adds to the scene"""
        # generate random string name for object if none provided by user
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


    def resizeScene(self):
        """Resize the graphics scene based on zoom value"""
        scale = self.state.zoom
        rect = self.itemsBoundingRect()
        self.setSceneRect(rect.x(), rect.y(), self.default_width / scale,
                self.default_height / scale)
        self.setLineDrawer()


    def setLineDrawer(self):
        """Initialize line drawer"""
        self.state.line_drawer.resize(self.width(), self.height())

        # change background of canvas to light gray
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.lightGray)
        self.state.line_drawer.setAutoFillBackground(True)
        self.state.line_drawer.setPalette(pal)
