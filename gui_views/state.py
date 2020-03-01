
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from graphic_scene import *
import sys, random

class State():
    def __init__(self):
        self.drag_state = True
        self.draw_wire_state = False
        self.coord_map = {} # Map coordinates to (user-defined) name of symobject
        self.sym_objects = {} # Map name to actual symobject (has coords)
        self.current_sym_object = None
        self.lines = []
        self.sub_object_lines = []
        self.line_drawer = None
        self.scene = None
        self.port_size = 10
        self.mainWindow = None

    # sets objects in scene as draggable or not draggable based on drag_state
    def setDragState(self):
        for object in self.sym_objects:
            self.sym_objects[object].setFlag(QGraphicsItem.ItemIsMovable, self.drag_state)

    # draws each line in lines using the QPen q
    def drawLines(self, q):
        if self.lines:
            for line in self.lines:
                q.drawLine(line[0].x(), line[0].y(), line[1].x(), line[1].y())


    # parses the sym_object dictionary to build the exported python file
    def getSymObjects(self):
        res = ""
        for object in self.sym_objects.values():
            if object.to_export:
                res += object.name + " = " + object.component_name + "("
                param = self.extractValue(object.parameters.items())
                if param:
                    res += param

                for child in object.connected_objects:
                    if not child:
                        break

                    res += object.name + "." + child + " = " + \
                            self.sym_objects[child].component_name + "("
                    param = extractValue(self.sym_objects[child].parameters.items())
                    if param:
                        res += param
        return res

    # extracts parameter values for a given sym_object
    def extractValue(self, parameters):
        param = ""
        for key, val in parameters:
            if val['Default'] != val['Value']:
                param += key + " = " + val['Value'] + ","
        param = param.rstrip(',')
        param += ")\n"
        return param
