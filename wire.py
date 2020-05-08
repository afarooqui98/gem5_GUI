from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from gui_views.dialogs import *

class Wire(QGraphicsItemGroup):
    def __init__(self, line, pen, state):
        super(Wire, self).__init__()
        # set line passed in
        graphicsLine = QGraphicsLineItem(line)
        graphicsLine.setPen(pen)
        self.parent_key = None
        self.child_key = None
        self.state = state

        endpoint_x = line.x2()
        endpoint_y = line.y2()

        # create both lines for arrowhead
        arrowhead1 = QLineF(endpoint_x, endpoint_y, endpoint_x + 5, endpoint_y + 5)
        arrowhead1.setAngle(line.angle() + 135)
        arrow1 = QGraphicsLineItem(arrowhead1)
        arrow1.setPen(pen)

        arrowhead2 = QLineF(endpoint_x, endpoint_y, endpoint_x + 5, endpoint_y + 5)
        arrowhead2.setAngle(line.angle() - 135)
        arrow2 = QGraphicsLineItem(arrowhead2)
        arrow2.setPen(pen)

        self.addToGroup(graphicsLine)
        self.addToGroup(arrow1)
        self.addToGroup(arrow2)

        # line only recieves double click events if it is selectable
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def mouseDoubleClickEvent(self, event):
        """register mouse press events"""

        # remove bounding box
        self.setSelected(False)

        parent = self.state.sym_objects[self.child_key[1]]
        child = self.state.sym_objects[self.parent_key[1]]

        # confirm deletion
        dialog = deleteWireDialog("Delete connection between " + parent.name +
                                "." + self.parent_key[2] + " and " + child.name
                                + "." + self.parent_key[3] + "?")

        # if yes, delete
        if dialog.exec_():
            self.deleteWire()

    def deleteWire(self):
        """delete all backend entries associate with connection and remove
        from scene"""

        parent = self.state.sym_objects[self.child_key[1]]
        child = self.state.sym_objects[self.parent_key[1]]
        parent.instance_ports[self.parent_key[2]]['Value'] = None
        del parent.ui_connections[self.parent_key]
        del child.ui_connections[self.child_key]
        self.state.scene.removeItem(self)
        self.state.addToHistory()
