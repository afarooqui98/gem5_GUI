import sys
from PySide2.QtWidgets import (QApplication, QLabel, QWidget, QMessageBox)
from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtCore import Qt, QPoint
from connection import *
from gui_views import state

class LineDrawer(QWidget):

    # constructor
    def __init__(self, state):
        super(LineDrawer, self).__init__()
        self.state = state
        self.initUI()
        self.setMouseTracking(True)

    # sets up the line position objects and state variable
    def initUI(self):
        self.pos1 = None
        self.pos2 = None
        self.draw_lines = 0
        self.line_done = 0
        self.line = None
        self.pen = QPen(Qt.black, 3)

    def mousePressEvent(self, event):
        if self.state.draw_wire_state:
            self.pos1 = event.pos()
            self.line_done = 0

    def mouseMoveEvent(self, event):
        if self.state.draw_wire_state and self.pos1:
            self.pos2 = event.pos()
            line = self.state.scene.addLine(self.pos1.x(), self.pos1.y(), self.pos2.x(),
                                 self.pos2.y(), self.pen)
            if self.line:
                self.state.scene.removeItem(self.line)
            self.line = line
            if not self.line_done:
                #self.update()
                pass

    def mouseReleaseEvent(self, event):
        if self.state.draw_wire_state:
            self.line_done = 1
            if self.setObjectConnection() < 0:
                ok = QMessageBox.about(self, "Alert", "Invalid line")
                # if not ok:
                #     pass
            self.pos1 = None
            self.pos2 = None
            self.draw_lines = 1
            self.state.scene.removeItem(self.line)
            self.line = None
            self.update()

    def update(self):
        self.state.drawLines(self.pen)


    # def paintEvent(self, event):
    #     #q = QPainter(self)
    #     if self.state.draw_wire_state:
    #         self.update()
    #     #draw port lines
    #     #q.setPen(QPen(Qt.black, 3))
    #     #currently drawing line
    #     if self.pos1 and self.pos2 and self.state.draw_wire_state:
    #         line = self.state.scene.addLine(self.pos1.x(), self.pos1.y(), self.pos2.x(),
    #                     self.pos2.y(), q.pen())
    #         if self.line:
    #             self.state.scene.removeItem(self.line)
    #         self.line = line
    #     #if self.draw_lines:
    #     self.state.drawLines(q)
            #self.draw_lines = 0

    def setObjectConnection(self):
        parent_loc = self.pos1
        child_loc = self.pos2
        parent, child = None, None
        parent_z_score = -1
        child_z_score = -1
        key = [None, None]
        for sym_object in self.state.sym_objects.values():
            key[0] = sym_object.scenePos().x()
            key[1] = sym_object.scenePos().y()
            if key[0] < parent_loc.x() and \
                    parent_loc.x() < key[0] + sym_object.width:
                if key[1] < parent_loc.y() and \
                        parent_loc.y() < key[1] + sym_object.height:
                    if sym_object.z > parent_z_score:
                        parent = sym_object
            if key[0] < child_loc.x() and \
                    child_loc.x() < key[0] + sym_object.width:
                if key[1] < child_loc.y() and \
                        child_loc.y() < key[1] + sym_object.height:
                    if sym_object.z > child_z_score:
                        child = sym_object
        #create connection, add to parent and child
        if not parent or not child:
            return -1
        self.pos1.setX(parent.scenePos().x() + parent.width / 2)
        self.pos1.setY(parent.scenePos().y() + parent.height / 2)
        self.pos2.setX(child.scenePos().x() + child.width / 2)
        self.pos2.setY(child.scenePos().y() + child.height / 2)
        parent.connections[("parent", child.name)] = Connection(self.pos1, self.pos2)
        child.connections[("child", parent.name)] = Connection(self.pos1, self.pos2)
        return 0
