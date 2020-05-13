import sys, string, random
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from connection import *
from gui_views import state
from m5_calls import portsCompatible

class LineDrawer(QWidget):

    # constructor
    def __init__(self, state):
        super(LineDrawer, self).__init__()
        self.state = state
        self.initUI()
        self.setMouseTracking(True)

    # sets up the line position objects and state variable
    def initUI(self):
        self.pos1 = None
        self.pos2 = None
        self.line = None
        self.pen = QPen(Qt.black, 2)

    # if clicking anywhere on the scene, unhighlight the currently selected
    # object and clear the attribute table
    def mousePressEvent(self, event):
        if self.state.draw_wire_state:
            self.pos1 = event.pos()
        else:
            self.state.removeHighlight()
            del self.state.selected_sym_objects[:]
            table = self.state.mainWindow.attributeView.attributeTable
            table.clear()
            table.setRowCount(0)

    def mouseMoveEvent(self, event):
        if self.state.draw_wire_state and self.pos1:
            self.pos2 = event.pos()
            line = self.state.scene.addLine(self.pos1.x(), self.pos1.y(), \
                         self.pos2.x(), self.pos2.y(), self.pen)

            if self.line:
                self.state.scene.removeItem(self.line)

            self.line = line
            self.line.setZValue(1000)

    def mouseReleaseEvent(self, event):
        if self.state.draw_wire_state and self.pos1 and self.pos2:
            valid_connection = self.setObjectConnection()
            self.pos1 = None
            self.pos2 = None
            if valid_connection < 0:
                if valid_connection == -1: #line badly drawn
                    ok = QMessageBox.warning(self.state.mainWindow,
                     "Alert!", "Invalid line")
                if valid_connection == -2: #port connection incompatible
                    ok = QMessageBox.warning(self.state.mainWindow,
                     "Error!", "You are drawing a line between\ntwo incompatible wires.")

            self.state.scene.removeItem(self.line)
            self.line = None
            self.update()
            self.state.mostRecentSaved = False

    def update(self):
        self.state.drawLines(self.pen)

    def contextMenuEvent(self, event):
        menu = QMenu()
        paste_action = menu.addAction("paste (Ctrl+v)")
        selected_action = menu.exec_(QCursor.pos())
        if selected_action == paste_action:
            self.state.mainWindow.buttonView.paste_button_pressed()

    def setObjectConnection(self):
        parent_loc = self.pos1
        child_loc = self.pos2
        parent, child = None, None
        parent_z_score = -1
        child_z_score = -1
        parent_port_num = 0
        parent_port_name = None
        child_port_num = 0
        child_port_name = None
        key = [None, None]
        for sym_object in self.state.sym_objects.values():
            count = 0
            delete_button_height = sym_object.delete_button.boundingRect().\
                                                                    height()
            next_y = delete_button_height
            for name, port, _ in sym_object.ui_ports:
                # change keys depending on where ports end up
                num_ports = len(sym_object.ui_ports)
                key[0] = sym_object.mapToScene(sym_object.boundingRect()).boundingRect().left() + sym_object.rect.boundingRect().width() * 3 / 4
                key[1] = sym_object.mapToScene(sym_object.boundingRect()).boundingRect().top() + next_y
                if key[0] < parent_loc.x() and \
                        parent_loc.x() < key[0] + port.rect().width():
                    if key[1] < parent_loc.y() and \
                            parent_loc.y() < key[1] + port.rect().height():
                        if sym_object.z > parent_z_score:
                            parent_z_score = sym_object.z
                            parent = sym_object
                            parent_port_num = count
                            parent_port_name = name
                if key[0] < child_loc.x() and \
                        child_loc.x() < key[0] + port.rect().width():
                    if key[1] < child_loc.y() and \
                            child_loc.y() < key[1] + port.rect().height():
                        if sym_object.z > child_z_score:
                            child_z_score = sym_object.z
                            child = sym_object
                            child_port_num = count
                            child_port_name = name
                next_y += (sym_object.height - delete_button_height) / num_ports
                count = count + 1

        #create connection, add to parent and child
        if not parent or not child:
            return -1

        key1 = ("parent", child.name, parent_port_name, child_port_name)
        key2 = ("child", parent.name, child_port_name, parent_port_name)
        if portsCompatible(parent.instance_ports[parent_port_name]['Value'],
            child.instance_ports[child_port_name]['Value']):
            parent.ui_connections[key1] = Connection(self.pos1, self.pos2,
                parent_port_num, child_port_num)
            child.ui_connections[key2] = Connection(self.pos1, self.pos2,
                parent_port_num, child_port_num)
            parent.instance_ports[parent_port_name]['Value'] = str(child.name) + "." + \
                str(child_port_name)
            self.state.addToHistory()
            return 0
        else:
            return -2
