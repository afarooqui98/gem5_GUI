from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from gui_views.dialogs import *

class Wire(QGraphicsLineItem):
    def __init__(self, line, pen, state):
        super(Wire, self).__init__()
        self.setPen(pen)
        self.setLine(line)
        self.parent_key = None
        self.child_key = None
        self.state = state

    def mousePressEvent(self, event):
        parent = self.state.sym_objects[self.child_key[1]]
        child = self.state.sym_objects[self.parent_key[1]]

        dialog = deleteWireDialog("Delete connection between " + parent.name +
                                "." + self.parent_key[2] + " and " + child.name
                                + "." + self.parent_key[3] + "?")

        if dialog.exec_():
            self.deleteWire()

    def deleteWire(self):
        parent = self.state.sym_objects[self.child_key[1]]
        child = self.state.sym_objects[self.parent_key[1]]
        parent.instance_ports[self.parent_key[2]]['Value'] = None
        del parent.ui_connections[self.parent_key]
        del child.ui_connections[self.child_key]
        self.state.scene.removeItem(self)
