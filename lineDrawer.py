import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

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
        self.lines = []

    def mousePressEvent(self, event):
        self.pos1 = event.pos()
        self.line_done = 0

    def mouseMoveEvent(self, event):
        self.pos2 = event.pos()
        if not self.line_done:
            self.update()

    def mouseReleaseEvent(self, event):
        self.line_done = 1
        self.lines.append((self.pos1, self.pos2))
        self.pos1 = None
        self.pos2 = None

    def paintEvent(self, event):
        if self.pos1 and self.pos2:
            q = QPainter(self)
            q.drawLine(self.pos1.x(), self.pos1.y(), self.pos2.x(), self.pos2.y())
            for line in self.lines:
                q.drawLine(line[0].x(), line[0].y(), line[1].x(), line[1].y())
