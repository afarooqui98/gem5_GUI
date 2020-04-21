from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class Wire(QGraphicsLineItem):
    def __init__(self, line, pen):
        super(Wire, self).__init__()
        self.setPen(pen)
        self.setLine(line)

    def mousePressEvent(self, event):
        print("pressed")
        super(Wire, self).mousePressEvent(event)
