try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

from graphic_field_scene_class import *
from graphic_system_item_class import *
from graphic_drag_label_class import *
from button import *
import sys, random


drag_state = True
draw_wire_state = False
sym_objects = {}
current_sym_object = None
lines = []
line_drawer = None
scene = None
port_size = 10
mainWindow = None

def setDragState():
    for object in sym_objects:
        sym_objects[object].setFlag(QGraphicsItem.ItemIsMovable, drag_state)

def drawLines(q):
    if lines:
        for line in lines:
            q.drawLine(line[0].x(), line[0].y(), line[1].x(), line[1].y())
