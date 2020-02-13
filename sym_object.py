try:
    from PyQt4.QtGui import *
except:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *

from field_class import *
from graphic_system_item_class import *
from lineDrawer import *
from PyQt5 import QtCore
import config


class SymObject(QGraphicsItemGroup):

    def __init__(self, x, y, width, height, scene, component_name):
        super(SymObject, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.connected_objects = []
        first = QGraphicsRectItem(scene.width()/2 - 100, scene.height()/2 - 50, width, height)
        second = QGraphicsTextItem(component_name)
        second.setPos(first.boundingRect().center() - second.boundingRect().center())

        self.addToGroup(first)
        self.addToGroup(second)
