from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from graphic_scene import *
from connection import *
from wire import *

import sys, random, os, logging, inspect

class State():
    def __init__(self, instances, catalog):
        self.drag_state = True # User can drag the objects
        self.select_state = True # User can select the objects
        self.draw_wire_state = False # User can draw wires
        self.sym_objects = {} # Map name to actual symobject (has coords)
        self.selected_sym_objects = []
        self.line_drawer = None
        self.scene = None
        self.mainWindow = None
        self.instances = instances
        self.catalog = catalog
        self.fileName = None
        self.copyState = False
        self.copied_objects = []
        self.mostRecentSaved = True
        self.zoom = 1

        # Store imported code in state
        self.imported_code = {}
        self.imported_code['headers'] = "import m5, sys, os"
        self.imported_code['headers'] += "\nfrom m5.objects import *"
        self.imported_code['headers'] += "\nfrom common import SimpleOpts"
        self.importedSymObjects = {}
        self.object_clicked = 0
        self.history_index = 0
        self.history = []

    # sets object flags in scene based on drag_state
    def setSymObjectFlags(self):
        for object in self.sym_objects.values():
            object.setFlag(QGraphicsItem.ItemIsMovable, self.drag_state)
            object.setFlag(QGraphicsItem.ItemIsSelectable, self.select_state)
            object.setFlag(QGraphicsItem.ItemIsFocusable, self.drag_state)
            object.setAcceptHoverEvents(self.drag_state)
            object.rect.setAcceptHoverEvents(self.drag_state)


    # draws each line in lines using the QPen p
    def drawLines(self, p):
        for object in self.sym_objects.values():
            for name, connection in object.ui_connections.items():
                if name[0] == "parent" and name[1] in self.sym_objects: #draw line once
                    self.drawConnection(p, connection, name, object.name)


    def drawConnection(self, p, connection, parent_key, parent_name):
        # remove old line if it exists
        if connection.line:
            self.scene.removeItem(connection.line)

        # instantiate a new line with connection coordinates
        line = QLineF(connection.parent_endpoint.x(), \
                connection.parent_endpoint.y(), connection.child_endpoint.x(), \
                    connection.child_endpoint.y())

        # create a new wire object so it can register mouse clicks
        wire = Wire(line, p, self)

        # add the wire to the scene
        self.scene.addItem(wire)

        connection.line = wire

        # set wire parameters that are needed for deletion
        wire.parent_key = parent_key
        wire.child_key = ("child", parent_name, parent_key[3], parent_key[2])

        connection.line.setZValue(1000)

    def removeHighlight(self):
        if len(self.selected_sym_objects):
            for sym_object in self.selected_sym_objects:
                sym_object.setIncomplete()
                if not sym_object.incomplete:
                    sym_object.rect.setBrush(QColor("White"))
                else:
                    sym_object.rect.setBrush(QColor("indianred"))

                sym_object.delete_button.hide()


    def updateObjs(self, imported_catalog, imported_instances, filename):
        """ Update the catalog and instance tree with new objects. """
        if filename in self.catalog:
            logging.debug("already imported file")
            return

        # Start to keep track of the imported objects
        if filename not in self.imported_code:
            self.imported_code[filename] = {}

        #Check if there are any duplicates in the imported objects
        for name in imported_instances.keys():
            if name in self.instances:
                imported_catalog[filename].pop(name, None)
                imported_instances.pop(name, None)
            elif name not in self.imported_code[filename]:
                #Store the src code in state
                src_code = inspect.getsource(imported_instances[name])
                self.imported_code[filename][name] = src_code
        self.catalog.update(imported_catalog)
        self.instances.update(imported_instances)
        self.mainWindow.repopulate(imported_catalog)


    def addObjectToCatalog(self, object, object_name):
        """add the passed in imported object to the catalog"""
        self.mainWindow.addImportedObjectToCatalog(object, object_name)

    def highlightIncomplete(self):
        """color the object red if a parameter is not set"""
        for object in self.sym_objects.values():
            object.setIncomplete()
            if object.incomplete:
                object.rect.setBrush(QColor("indianred"))

    def addToHistory(self):
        state_pos = len(self.history) - self.history_index - 1
        #not most current state
        if state_pos > 0:
            #remove elements from history
            for i in range(state_pos):
                self.history.pop()
        history = self.mainWindow.buttonView.getOutputData(self.sym_objects)
        self.history.append(history)
        self.history_index = len(self.history) - 1
        if self.history_index:
            self.mainWindow.buttonView.undo.setEnabled(True)
            self.mainWindow.buttonView.redo.setEnabled(False)
            self.mostRecentSaved = False

#finds the gem5 path
def get_path():
    gem5_parent_dir = os.getenv("GEM5_HOME")
    #if parent dir not explicitly set, procure it from executable path
    if not gem5_parent_dir:
        gem5_parent_dir = sys.executable.split("gem5")[0]
    for root, dirs, files in os.walk(gem5_parent_dir, topdown=False):
        for name in dirs:
            abs_path = os.path.join(root, name)
            if abs_path.endswith("gem5/configs"):
                os.environ['gem5_path'] = abs_path
