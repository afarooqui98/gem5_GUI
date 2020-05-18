from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from gui_views.dialogs import *

"""This class holds the visual representation of a wire connecting two ports.
It is composed of a line and an arrow head made up of two lines. This class
handles inspection and deletion of wires."""

class Wire(QGraphicsItemGroup):
    def __init__(self, line, pen, state):
        super(Wire, self).__init__()
        # set line passed in
        graphicsLine = QGraphicsLineItem(line)
        graphicsLine.setPen(pen)
        self.parent_key = None
        self.child_key = None
        self.state = state

        self.addToGroup(graphicsLine)

        # create both lines for arrowhead
        self.createArrowHead(line, 135, pen)
        self.createArrowHead(line, -135, pen)

    def createArrowHead(self, line, angle, pen):
        """Create one of the two lines composing the arrowhead"""
        # get the endpoints of the line
        x = line.x2()
        y = line.y2()

        # arrow line construction
        arrowhead = QLineF(x, y, x + 5, y + 5)
        arrowhead.setAngle(line.angle() + angle)
        arrow = QGraphicsLineItem(arrowhead)
        arrow.setPen(pen)
        self.addToGroup(arrow)


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
            # reset port values to default
            parent.instance_ports[self.parent_key[2]]['Value'] = \
                    parent.instance_ports[self.parent_key[2]]['Default']
            child.instance_ports[self.child_key[2]]['Value'] = \
                    child.instance_ports[self.child_key[2]]['Default']
            #delete connection from each object's connection dictionary
            del parent.ui_connections[self.parent_key]
            del child.ui_connections[self.child_key]
            #remove item from scene, add action to history
            self.state.scene.removeItem(self)
            self.state.addToHistory()

    # TODO: fix and finish this function
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
