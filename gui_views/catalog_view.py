from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *

import sys, random
import copy
from gui_views import config
import json

class CatalogView(): #dropdown and search bar
    def __init__(self, layout, catalog):
        self.catalog = catalog
        #search bar
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Search for an object here!")
        layout.addWidget(self.edit)

        #dropdown for SimObjects
        self.treeWidget = QTreeWidget()
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Name")
        layout.addWidget(self.treeWidget)

        #handlers
        self.edit.textChanged.connect(self.searchItem)
        self.treeWidget.itemDoubleClicked.connect(self.createSymObject)

    #this creates a new symobject at some point in the CanvasView
    def createSymObject(self, item):
        if item.parent() is None:
            return

        name, ok = QInputDialog.getText(config.mainWindow, "Alert", "New SimObject name:")
        if not ok:
            return

        config.current_sym_object = \
            config.scene.addObjectToScene("component", item.text(0), name)
        config.current_sym_object.parameters = \
            copy.deepcopy(self.catalog[item.parent().text(0)][item.text(0)])

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
                # hide and expand top-level item based on if sub-level item
                #   is a match
                item.setHidden(not not_found)
                item.setExpanded(not_found)
