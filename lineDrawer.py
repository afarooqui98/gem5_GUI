import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
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
        if self.pos1 and self.pos2:
            q.drawLine(self.pos1.x(), self.pos1.y(), self.pos2.x(), self.pos2.y())
        config.drawLines(q)
