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

    def contextMenuEvent(self, event):
        menu = QMenu()
        delete_action = menu.addAction("delete wire")
        inspect_action = menu.addAction("inspect wire")
        selected_action = menu.exec_(QCursor.pos())
        if selected_action == delete_action:
            self.deleteWire()
        elif selected_action == inspect_action:
            pass

    def deleteWire(self):
        """delete all backend entries associate with connection and remove
        from scene"""
        parent = self.state.sym_objects[self.child_key[1]]
        child = self.state.sym_objects[self.parent_key[1]]

        # confirm deletion
        dialog = deleteWireDialog("Delete connection between " + parent.name +
                                "." + self.parent_key[2] + " and " + child.name
                                + "." + self.parent_key[3] + "?")
        # if yes, delete
        if dialog.exec_():
            parent = self.state.sym_objects[self.child_key[1]]
            child = self.state.sym_objects[self.parent_key[1]]
            parent.instance_ports[self.parent_key[2]]['Value'] = None
            del parent.ui_connections[self.parent_key]
            del child.ui_connections[self.child_key]
            self.state.scene.removeItem(self)

    def inspect(self):
        pass
        # parent = self.state.sym_objects[self.child_key[1]]
        # child = self.state.sym_objects[self.parent_key[1]]
        # parent_port = self.parent_key[2]
        # child_port = self.parent_key[3]
        #
        # print("parent: " + parent.name)
        # print("port: " + parent.instance_ports[parent_port]['Description'])
        #
        # print("child: " + child.name)
        # print("port: " + child.instance_ports[child_port]['Description'])

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
