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


class SymObject():

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.connected_objects = []
