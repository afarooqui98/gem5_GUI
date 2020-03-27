from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *

import sys, random
import copy
from gui_views import state
import json

class CatalogView(): #dropdown and search bar
    def __init__(self, layout, catalog, state):
        self.state = state
        self.catalog = catalog
        #search bar
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Search for an object here!")

        #adding fix width on one of the widgets in the catalog area will
        #implicitly set a fixed width on the rest of the widgets
        #we do this so that the catalog retains its original dimensions while
        #resizing the window
        self.edit.setFixedWidth(250)

        layout.addWidget(self.edit)

        #dropdown for SimObjects
        self.treeWidget = QTreeWidget()
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Name")
        self.treeWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.treeWidget)

        #handlers
        self.edit.textChanged.connect(self.searchItem)
        self.treeWidget.itemClicked.connect(self.removeHighlight)
        self.treeWidget.itemDoubleClicked.connect(self.createSymObject)

    def removeHighlight(self, item):
        if self.state.current_sym_object:
            print("creating new obj, unhighlighting previous selection")
            self.state.current_sym_object.rect.setBrush(QColor("White"))

    #this creates a new symobject at some point in the CanvasView
    def createSymObject(self, item):
        if item.parent() is None:
            return

        name, ok = QInputDialog.getText(self.state.mainWindow, "Alert", \
                                        "New SimObject name:")
        if not ok:
            return

        if name in self.state.sym_objects:
            ok = QMessageBox.about(self.state.mainWindow, "Alert", \
                            "SimObject with name: " + name + " already exists!")
            if not ok:
                pass
            return

        self.state.current_sym_object = \
            self.state.scene.addObjectToScene("component", item.text(0), name)
        self.state.current_sym_object.parameters = \
            copy.deepcopy(self.catalog[item.parent().text(0)][item.text(0)]['params'])
        self.state.current_sym_object.ports = \
            copy.deepcopy(self.catalog[item.parent().text(0)][item.text(0)]['ports'])
        self.state.current_sym_object.SimObject = \
            copy.deepcopy(
            self.state.instances[self.state.current_sym_object.component_name])
        self.state.current_sym_object.initPorts()
        self.state.current_sym_object.instantiateSimObject()


    # make tree view searchable
    def searchItem(self):
        """
        Searches treeview whenever a user types something in the search bar
        """
        # Get string in the search bar and use treeview's search fn
        search_string = self.edit.text()
        match_items = self.treeWidget.findItems(search_string, Qt.MatchContains
                                                | Qt.MatchRecursive)

        root = self.treeWidget.invisibleRootItem()
        child_count = root.childCount()

        # Iterate through top-level items
        for i in range(child_count):
            item = root.child(i)
            if len(match_items) == 0: # Hide all items if no matches
                item.setHidden(True)

            elif search_string == "": # if empty string don't hide or expand
                item.setHidden(False)
                item.setExpanded(False)

            else:
                # Go through sub items for each top-level item
                gchild_count = item.childCount()
                # see if any sub item is a match
                not_found = False
                for j in range(gchild_count):
                    grand_item = item.child(j)
                    not_found = not_found or (grand_item in set(match_items))
                    grand_item.setHidden(grand_item not in set(match_items))
                # hide and expand top-level item based on if sub-level item
                #   is a match
                item.setHidden(not not_found)
                item.setExpanded(not_found)
