
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from graphic_scene import *
from connection import *
import sys, random, os

class State():
    def __init__(self, instances, catalog):
        self.drag_state = True
        self.draw_wire_state = False
        self.coord_map = {} # Map coordinates to name of symobject
        self.sym_objects = {} # Map name to actual symobject (has coords)
        self.current_sym_object = None
        self.line_drawer = None
        self.scene = None
        self.mainWindow = None
        self.instances = instances
        self.catalog = catalog
        self.buttonView = None
        self.fileName = None

    # sets objects in scene as draggable or not draggable based on drag_state
    def setDragState(self):
        for object in self.sym_objects.values():
            object.setFlag(QGraphicsItem.ItemIsMovable, self.drag_state)

    # draws each line in lines using the QPen p
    def drawLines(self, p):
        for object in self.sym_objects.values():
            for name, connection in object.connections.items():
                if name[0] == "parent": #don't need to draw line twice
                    self.drawConnection(p, connection)


    def drawConnection(self, p, connection):
        if connection.line:
            self.scene.removeItem(connection.line)
        connection.line = self.scene.addLine(connection.parent_endpoint.x(), \
        connection.parent_endpoint.y(), connection.child_endpoint.x(), \
        connection.child_endpoint.y(), p)

        connection.line.setZValue(1000)


def get_path():
    gem5_parent_dir = sys.executable.split("gem5")[0]
    for root, dirs, files in os.walk(gem5_parent_dir, topdown=False):
        for name in dirs:
            abs_path = os.path.join(root, name)
            if abs_path.endswith("gem5/configs"):
                os.environ['gem5_path'] = abs_path
