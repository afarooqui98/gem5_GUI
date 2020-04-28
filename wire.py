from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from gui_views.dialogs import *

class Wire(QGraphicsLineItem):
    def __init__(self, line, pen, state):
        super(Wire, self).__init__()
        # set pen and line passed in
        self.setPen(pen)
        self.setLine(line)
        self.parent_key = None
        self.child_key = None
        self.state = state

        # line only recieves double click events if it is selectable
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def mouseDoubleClickEvent(self, event):
        """register mouse press events"""

        # remove bounding box
        self.setSelected(False)

        parent = self.state.sym_objects[self.child_key[1]]
        child = self.state.sym_objects[self.parent_key[1]]

        # confirm deletion
        dialog = deleteWireDialog("Delete connection between " +
                                parent.display_name + "." + self.parent_key[2]
                                + " and " + child.display_name + "." +
                                self.parent_key[3] + "?")

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
