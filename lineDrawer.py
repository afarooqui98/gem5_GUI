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
            line = self.state.scene.addLine(self.pos1.x(), self.pos1.y(), \
                        self.pos2.x(), self.pos2.y(), self.pen)
            if self.line:
                self.state.scene.removeItem(self.line)
            self.line = line

    def mouseReleaseEvent(self, event):
        if self.state.draw_wire_state and self.pos1 and self.pos2:
            self.line_done = 1
            if self.setObjectConnection() < 0:
                ok = QMessageBox.about(self, "Alert", "Invalid line")

            self.pos1 = None
            self.pos2 = None
            self.draw_lines = 1
            self.state.scene.removeItem(self.line)
            self.line = None
            self.update()

    def update(self):
        self.state.drawLines(self.pen)

    def setObjectConnection(self):
        parent_loc = self.pos1
        child_loc = self.pos2
        parent, child = None, None
        parent_z_score = -1
        child_z_score = -1
        parent_port_num = 0
        child_port_num = 0
        key = [None, None]
        for sym_object in self.state.sym_objects.values():
            count = 0
            delete_button_height = sym_object.deleteButton.boundingRect().height()
            next_y = delete_button_height
            for port in sym_object.sym_ports:
                # change keys depending on where ports end up
                num_ports = len(sym_object.sym_ports)
                key[0] = sym_object.scenePos().x() + sym_object.width * 3 / 4
                key[1] = sym_object.scenePos().y() + next_y
                # print(key[0], parent_loc.x(), key[0] + 25)
                # print(key[1], parent_loc.y(), key[1] + 10)
                # print(key[0], child_loc.x(), key[0] + 25)
                # print(key[1], child_loc.y(), key[1] + 10)
                if key[0] < parent_loc.x() and \
                        parent_loc.x() < key[0] + port.rect().width():
                    if key[1] < parent_loc.y() and \
                            parent_loc.y() < key[1] + port.rect().height():
                        if sym_object.z > parent_z_score:
                            parent_z_score = sym_object.z
                            parent = sym_object
                            parent_port_num = count
                if key[0] < child_loc.x() and \
                        child_loc.x() < key[0] + port.rect().width():
                    if key[1] < child_loc.y() and \
                            child_loc.y() < key[1] + port.rect().height():
                        if sym_object.z > child_z_score:
                            child_z_score = sym_object.z
                            child = sym_object
                            child_port_num = count
                next_y += (sym_object.height - delete_button_height) / num_ports
                count = count + 1

        #create connection, add to parent and child
        if not parent or not child:
            return -1
        # self.pos1.setX(parent.scenePos().x() + parent.width / 2)
        # self.pos1.setY(parent.scenePos().y() + parent.height / 2)
        # self.pos2.setX(child.scenePos().x() + child.width / 2)
        # self.pos2.setY(child.scenePos().y() + child.height / 2)
        key1 = ("parent", child.name)
        key2 = ("child", parent.name)
        parent.connections[key1] = Connection(self.pos1, self.pos2, parent_port_num, child_port_num)
        child.connections[key2] = Connection(self.pos1, self.pos2, parent_port_num, child_port_num)
        return 0
