
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from lineDrawer import *
from PySide2 import QtCore
from gui_views import config
from sym_object import *
import string

class GraphicsScene(QGraphicsScene):
    """this class provides a scene to manage objects"""

    # constructor
    def __init__(self, x, y, width, height):
        super(GraphicsScene, self).__init__(x, y, width, height)
        config.line_drawer = LineDrawer()
        config.line_drawer.resize(self.width(), self.height())
        self.addWidget(config.line_drawer)

    # load object from saved UI file
    def loadSavedObject(self, type, name, newObject):

        x = newObject["x"]
        y = newObject["y"]
        component_name = newObject["component_name"]
        parameters = newObject["parameters"]

        if component_name == "System":
            new_object = SymObject(0, 0, 500, 500, self, component_name, name,
                                    True)
        else:
            new_object = SymObject(x, y, 120, 60, self, component_name, name,
                                    True)

        new_object.parameters = parameters

        # add new object to backend datastructures
        config.sym_objects[name] = new_object
        config.current_sym_object = new_object
        self.addItem(new_object)
        return new_object

    def addObjectToScene(self, type, component_name, name):

        # generate random string name for object
        if not name:
            name = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(7))

        # add object rectangle to scene
        if component_name == "System":
            new_object = SymObject(0, 0, 500, 500, self, component_name, name,
                                    False)
        else:
            new_object = SymObject(0, 0, 120, 60, self, component_name, name,
                                    False)

        config.sym_objects[name] = new_object
        config.current_sym_object = new_object
        self.addItem(new_object)
        return new_object

    # if an object is dragged into the scene
    def dragEnterEvent(self,event):
        if config.drag_state:
            event.accept()

    # if an object is dragged around on the scene
    def dragMoveEvent(self,event):
        if config.drag_state:
            event.accept()

    # if an object is dropped on the scene
    def dropEvent(self,event):
        if config.drag_state:
            event.accept()
        else:
            return

    # paint event to draw lines
    def paintEvent(self, event):
        q = QPainter(self)
        config.drawLines(q, config.lines)
