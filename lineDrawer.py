import sys
from PySide2.QtWidgets import (QApplication, QLabel, QWidget, QMessageBox)
from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtCore import Qt, QPoint
from connection import *
from gui_views import config

class LineDrawer(QWidget):

    # constructor
    def __init__(self):
        super(LineDrawer, self).__init__()
        self.initUI()
        self.setMouseTracking(True)

    # sets up the line position objects and state variable
    def initUI(self):
        self.pos1 = None
        self.pos2 = None
        self.line_done = 0

    def mousePressEvent(self, event):
        if config.draw_wire_state:
            self.pos1 = event.pos()
            self.line_done = 0

    def mouseMoveEvent(self, event):
        if config.draw_wire_state:
            self.pos2 = event.pos()
            if not self.line_done:
                self.update()

    def mouseReleaseEvent(self, event):
        if config.draw_wire_state:
            self.line_done = 1
            if self.setObjectConnection() >= 0:
                config.lines.append((self.pos1, self.pos2))
                print(config.current_sym_object.connections)
            else:
                ok = QMessageBox.about(self, "Alert", "Invalid line")
                if not ok:
                    pass
            self.pos1 = None
            self.pos2 = None


    def paintEvent(self, event):
        q = QPainter(self)
        if config.draw_wire_state:
            self.update()
        #draw port lines
        q.setPen(QPen(Qt.black, 3))
        if self.pos1 and self.pos2:
            q.drawLine(self.pos1.x(), self.pos1.y(), self.pos2.x(),
                        self.pos2.y())
        config.drawLines(q, config.lines)

        #draw sub object lines
        q.setPen(QPen(Qt.black, 2, Qt.DotLine))
        config.drawLines(q, config.sub_object_lines)


    def setObjectConnection(self):
        parent_loc = self.pos1
        child_loc = self.pos2
        parent, child = None, None
        for key, val in config.coord_map.items():
            sym_object = config.sym_objects[val]
            if key[0] < parent_loc.x() and \
                    parent_loc.x() < key[0] + sym_object.width:
                if key[1] < parent_loc.y() and \
                        parent_loc.y() < key[1] + sym_object.height:
                    parent = sym_object
            if key[0] < child_loc.x() and \
                    child_loc.x() < key[0] + sym_object.width:
                if key[1] < child_loc.y() and \
                        child_loc.y() < key[1] + sym_object.height:
                    child = sym_object
        #create connection, add to parent and child
        if not parent or not child:
            return -1
        self.pos1.setX(parent.x + parent.width / 2)
        self.pos1.setY(parent.y + parent.height / 2)
        self.pos2.setX(child.x + child.width / 2)
        self.pos2.setY(child.y + child.height / 2)
        parent.connections[child.name] = Connection(self.pos1, self.pos2)
        child.connections[parent.name] = Connection(self.pos1, self.pos2)
        return 0

    # connects a parent and child object with a dotted line
    def connectSubObject(self, parent_name, child_name):
        parent = config.sym_objects[parent_name]
        child = config.sym_objects[child_name]
        #implement later
        #x1, y1, x2, y2 = self.calculateShortestDistance(parent_name,
        #                                                    child_name)
        pos1 = QPoint()
        pos2 = QPoint()
        # draw line from middle of parent to middle of child
        pos1.setX(parent.x + parent.width / 2)
        pos1.setY(parent.y + parent.height / 2)
        pos2.setX(child.x + child.width / 2)
        pos2.setY(child.y + child.height / 2)
        # add line to sub_object_lines list
        config.sub_object_lines.append((pos1, pos2))
        # triggers paint event to redraw scene
        self.update()

    # used to draw line between parent and child (unimplemented)
    def calculateShortestDistance(self, parent_name, child_name):
        pass
