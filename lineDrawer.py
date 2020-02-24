import sys
from PySide2.QtWidgets import (QApplication, QLabel, QWidget)
from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtCore import Qt, QPoint
import config

class LineDrawer(QWidget):

    # constructor
    def __init__(self):
        super().__init__()
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
            config.lines.append((self.pos1, self.pos2))
            self.pos1 = None
            self.pos2 = None

    def paintEvent(self, event):
        q = QPainter(self)

        #draw port lines
        q.setPen(QPen(Qt.black, 3))
        if self.pos1 and self.pos2:
            q.drawLine(self.pos1.x(), self.pos1.y(), self.pos2.x(),
                        self.pos2.y())
        config.drawLines(q, config.lines)

        #draw sub object lines
        q.setPen(QPen(Qt.black, 2, Qt.DotLine))
        config.drawLines(q, config.sub_object_lines)


    # connects a parent and child object with a dotted line
    def connectSubObject(self, parent_name, child_name):
        parent = config.sym_objects[parent_name]
        child = config.sym_objects[child_name]
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
