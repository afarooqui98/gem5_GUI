import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
import config

class LineDrawer(QWidget):
    distance_from_center = 0
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

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
            config.lines.append((self.pos1, self.pos2))
            self.pos1 = None
            self.pos2 = None

    def paintEvent(self, event):
        q = QPainter(self)

        #draw port lines
        q.setPen(QPen(Qt.black, 3))
        if self.pos1 and self.pos2:
            q.drawLine(self.pos1.x(), self.pos1.y(), self.pos2.x(), self.pos2.y())
        config.drawLines(q, config.lines)

        #draw sub object lines
        q.setPen(QPen(Qt.black, 2, Qt.DotLine))
        config.drawLines(q, config.sub_object_lines)

    def connectSubObject(self, parent_name, child_name):
        parent = config.sym_objects[parent_name]
        child = config.sym_objects[child_name]
        #x1, y1, x2, y2 = self.calculateShortestDistance(parent_name, child_name)
        pos1 = QPoint()
        pos2 = QPoint()
        pos1.setX(parent.x + parent.width / 2)
        pos1.setY(parent.y + parent.height / 2)
        pos2.setX(child.x + child.width / 2)
        pos2.setY(child.y + child.height / 2)
        config.sub_object_lines.append((pos1, pos2))
        self.update()

    def calculateShortestDistance(self, parent_name, child_name):
        pass
