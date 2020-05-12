
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphic_scene import *
from gui_views.catalog_view import *
from gui_views.button_view import *
from gui_views.catalog_view import *
from gui_views.attribute_view import *
from gui_views.debug_view import *
from gui_views.toolbar_view import *
from gui_views.state import *
from m5_calls import isSimObjectParam

import sys, random
import copy
import json
import functools
import logging


class MainWindow(QMainWindow):
    """this class creates the main window"""

    def __init__(self, catalog, instances):
        super(MainWindow, self).__init__()
        self.state = State(instances, catalog)
        #self.setWindowTitle("gem5 GUI | Untitled")
        self.main = QWidget()
        self.catalog = catalog
        self.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout = QVBoxLayout()
        self.gridLayout.setObjectName("gridLayout")

        #add button view
        self.buttonView = ButtonView(self.gridLayout, self.state, self)
        #add toolbar view
        self.toolbarView = ToolBarView(self.gridLayout, self.state, self)
        #add catalog view
        self.catalogView = CatalogView(self.gridLayout, catalog, self.state)
        #add attributes
        self.attributeView = AttributeView(self.gridLayout, self.state)

        self.state.scene = GraphicsScene(0,0, 1750, 1250, self.state)
        self.graphics_view = QGraphicsView(self.state.scene)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.graphics_view)

        #add debug window
        self.debug_hidden = False # Flag for toggling debug widget
        self.debug_widget = DebugWidget(self.state)
        self.layout.addWidget(self.debug_widget)
        self.toggleDebug()

        self.main.setLayout(self.layout)
        self.setCentralWidget(self.main)

        # populate treeview
        self.populate()
        self.catalogView.treeWidget.itemClicked.connect(self.treeWidgetClicked)

    def toggleInspect(self, isObject, attributeList):
        if self.inspect_hidden:
            self.inspect_widget.populate(isObject, attributeList)
            self.inspect_widget.show()
        else:
            self.inspect_widget.clear()
            self.inspect_widget.hide()

    def toggleDebug(self):
        """ Enables or disables the debug widget from being shown"""
        if self.debug_hidden:
            self.debug_widget.show()
        else:
            self.debug_widget.hide()
        self.debug_hidden = not self.debug_hidden

    def createDropDown(self, value, table, param):
        """ Create the drop down for simobject parameters in the table view """
        comboBox = QComboBox()
        # Create list for dropdown including the default value
        dropdown_list = copy.deepcopy(\
            self.state.selected_sym_objects[0].connected_objects)
        if value in dropdown_list:
            dropdown_list.remove(value)

        # Make whatever value or default value the first option
        dropdown_list = [value] + dropdown_list

        #Check if param is req
        if dropdown_list[0] == 'None':
              cbstyle = " QComboBox {"
              cbstyle += " background: red;"
              cbstyle += "}"
              comboBox.setStyleSheet(cbstyle)

        comboBox.addItems(dropdown_list)
        # Add event handler to update values in the symobject structure
        comboBox.currentTextChanged.connect(functools.partial(\
            self.attributeView.modifyParam, param))
        table.setCellWidget(table.rowCount() - 1, 1, comboBox)

    def addRow(self, param, value, isTreeWidgetClick, isSimObject):
        """ Adds the param and value to a row of the table."""
        table = self.attributeView.attributeTable
        table.insertRow(table.rowCount())

        # set column 0 value with param
        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(param))
        cell = table.item(table.rowCount() - 1, 0)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

        if param != "Name" and param != "Child Objects":
            cell.setToolTip(self.attributes[param]["Description"])

        # set column 1 value with value
        table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(value))
        if isSimObject: #add a drop down of child objects
            self.createDropDown(value, table, param)

        cell = table.item(table.rowCount() - 1, 1)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)
        if not isTreeWidgetClick and value == 'None': # check if param is req
            cell.setBackground(QColor("indianred"))
            self.state.highlightIncomplete()


    def treeWidgetClicked(self, item, name):
        self.populateAttributes(item, name, True)

    def populateAttributes(self, item, name, isTreeWidgetClick):
        """Populate the attribute table holding info for an objects
            params and children"""
        table = self.attributeView.attributeTable
        table.clear()
        table.setRowCount(0)

        # If there is an object being viewed on the board display the name and
        #   connected objects as well
        if len(self.state.selected_sym_objects) == 1:
            cur_object = self.state.selected_sym_objects[0]
            self.addRow("Name", cur_object.name,
                        isTreeWidgetClick, False)
            self.addRow("Child Objects",
                        ", ".join(cur_object.connected_objects),
                        isTreeWidgetClick, False)
        if item:
            if item.parent() is None or item.text(0) in \
                                                self.state.importedSymObjects:
                return
            self.attributes = \
                self.catalog[item.parent().text(0)][item.text(0)]['params']
        else:
            # only load from param list if there is a sym object in the context
            if len(self.state.selected_sym_objects) == 1 or \
                self.state.selected_sym_objects[0].component_name == name:
                self.attributes = \
                    self.state.selected_sym_objects[0].instance_params
            else: # TODO: check when would this branch happen??
                logging.debug("filling in name branch")
                self.attributes = self.catalog[name]

        # display the param name and values
        for attribute in sorted(self.attributes.keys()):
            # Simobject params are special cases with dropdowns in the table
            isSim = False
            if len(self.state.selected_sym_objects) > 0:
                isSim = self.state.selected_sym_objects[0] and \
                    isSimObjectParam(self.attributes[attribute])
            self.addRow(attribute, str(self.attributes[attribute]["Value"]),
                                                    isTreeWidgetClick, isSim)

    def repopulate(self, imported_catalog):
        """Adds newly imported sub_objs and updates the catalog"""
        # Go through every inheritable sym-object
        for item in sorted(imported_catalog.keys()):
            tree_item = QTreeWidgetItem([item])
            # Go through every specialized sym-object
            for sub_item in sorted(imported_catalog[item].keys()):
                tree_item.addChild(QTreeWidgetItem([sub_item]))
            self.catalogView.treeWidget.addTopLevelItem(tree_item)
        self.catalog.update(imported_catalog)

    def populate(self):
        """ This function populates the tree view with sym-objects"""
        # Go through every inheritable sym-object
        for item in sorted(self.catalog.keys()):
            tree_item = QTreeWidgetItem([item])
            # Go through every specialized sym-object
            for sub_item in sorted(self.catalog[item].keys()):
                tree_item.addChild(QTreeWidgetItem([sub_item]))
            self.catalogView.treeWidget.addTopLevelItem(tree_item)

    def addImportedObjectToCatalog(self, object, object_name):
        """create new entry in catalog for imported objects"""
        parent_item = self.catalogView.treeWidget.findItems(\
            "Imported Objects", Qt.MatchContains)

        if not parent_item:
            self.catalog["Imported Objects"] = {}
            tree_item = QTreeWidgetItem(["Imported Objects"])
            self.catalog["Imported Objects"][object_name] = object
            tree_item.addChild(QTreeWidgetItem([object_name]))
            self.catalogView.treeWidget.addTopLevelItem(tree_item)
        else:
            parent_item[0].addChild(QTreeWidgetItem([object_name]))

    def closeEvent(self, event):
        """When user tries to exit, check if changes need to be saved
            before closing"""
        if not self.state.mostRecentSaved:
            self.dialog = saveChangesDialog("closing", self.state)
            if self.dialog.exec_():
                self.buttonView.save_button_pressed()

if __name__ == "__m5_main__":
    import sys
    import os
    sys.path.append(os.getenv('gem5_path'))
    import m5.objects
    from common import ObjectList
    from m5_calls import get_obj_lists

    # use gem5 to get list of objects
    obj_tree, instance_tree = get_obj_lists()
    gui_application = QApplication() #create new application
    #create new instance of main window
    main_window = MainWindow(obj_tree, instance_tree)
    main_window.state.mainWindow = main_window
    main_window.setWindowTitle("gem5 GUI | Untitled")
    main_window.show() #make instance visible
    main_window.raise_() #raise instance to top of window stack
    gui_application.exec_() #monitor application for events
    gui_application.quit()
