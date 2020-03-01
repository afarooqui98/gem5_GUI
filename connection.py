from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtWidgets import (QApplication, QLabel, QWidget, QMessageBox)

# holds a parent-child connection between two sym_objects. The parent and child
# share access to this class object in order to have access to the line
# endpoints for redrawing purposes. More functionality to be added later
class Connection:

    def __init__(self, parent_endpoint, child_endpoint):
        self.parent_endpoint = parent_endpoint
        self.child_endpoint = child_endpoint

    # sets new endpoints for the line (None passed in if unmodified)
    def setEndpoints(self, parent_endpoint, child_endpoint):
        if parent_endpoint is not None:
            self.parent_endpoint = parent_endpoint
        if child_endpoint is not None:
            self.child_endpoint = child_endpoint

    def drawConnection(self):
        self.update()

    def paintEvent(self, event):
        q = QPainter(self)
        q.setPen(QPen(Qt.black, 3))
        q.drawLine(self.parent_endpoint.x(), self.parent_endpoint.y(), self.child_endpoint.x(), self.child_endpoint.y())
