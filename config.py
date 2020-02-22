
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from graphic_scene import *
from button import *
import sys, random


drag_state = True
draw_wire_state = False
coord_map = {} # Map coordinates to (user-defined) name of symobject
sym_objects = {} # Map name to actual symobject (has coords)
current_sym_object = None
lines = []
sub_object_lines = []
line_drawer = None
scene = None
port_size = 10
mainWindow = None

# sets objects in scene as draggable or not draggable based on drag_state
def setDragState():
    for object in sym_objects:
        sym_objects[object].setFlag(QGraphicsItem.ItemIsMovable, drag_state)

# draws each line in lines using the QPen q
def drawLines(q, lines):
    if lines:
        for line in lines:
            q.drawLine(line[0].x(), line[0].y(), line[1].x(), line[1].y())


# parses the sym_object dictionary to build the exported python file
def getSymObjects():
    res = ""
    for object in sym_objects.values():
        if object.to_export:
            res += object.name + " = " + object.component_name + "("
            param = extractValue(object.parameters.items())
            if param:
                res += param

            connected_objects = object.connected_objects.split(",")
            for child in connected_objects:
                if not child:
                    break

                res += object.name + "." + child + " = " + \
                        sym_objects[child].component_name + "("
                param = extractValue(sym_objects[child].parameters.items())
                if param:
                    res += param
    return res

# extracts parameter values for a given sym_object
def extractValue(parameters):
    param = ""
    for key, val in parameters:
        if val['Default'] != val['Value']:
            param += key + " = " + val['Value'] + ","
    param = param.rstrip(',')
    param += ")\n"
    return param
