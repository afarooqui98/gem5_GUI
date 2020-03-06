
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from graphic_scene import *
from connection import *
import sys, random

class State():
    def __init__(self):
        self.drag_state = True
        self.draw_wire_state = False
        self.coord_map = {} # Map coordinates to name of symobject
        self.sym_objects = {} # Map name to actual symobject (has coords)
        self.current_sym_object = None
        self.line_drawer = None
        self.scene = None
        self.mainWindow = None

    # sets objects in scene as draggable or not draggable based on drag_state
    def setDragState(self):
        for object in self.sym_objects.values():
            object.setFlag(QGraphicsItem.ItemIsMovable, self.drag_state)

    # draws each line in lines using the QPen p
    def drawLines(self, p):
        for object in self.sym_objects.values():
            for name, connection in object.connections.items():
                self.drawConnection(p, connection)


    def drawConnection(self, p, connection):
        line = self.scene.addLine(connection.parent_endpoint.x(), \
        connection.parent_endpoint.y(), connection.child_endpoint.x(), \
        connection.child_endpoint.y(), p)
        if connection.line:
            self.scene.removeItem(connection.line)
        connection.line = line
