
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphic_scene import *
from gui_views.catalog_view import *
from gui_views.button_view import *
from gui_views.catalog_view import *
from gui_views.attribute_view import *
from gui_views.state import *

import sys, random
import copy
import json

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
        #add catalog view
        self.catalogView = CatalogView(self.gridLayout, catalog, self.state)
        #add attributes
        self.attributeView = AttributeView(self.gridLayout, self.state)

        self.state.scene = GraphicsScene(0,0, 1750, 1250, self.state)
        self.graphics_view = QGraphicsView(self.state.scene)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.graphics_view)

        self.main.setLayout(self.layout)
        self.setCentralWidget(self.main)

        # populate treeview
        self.populate()
        self.catalogView.treeWidget.itemClicked.connect(self.treeWidgetClicked)

    def addRow(self, value1, value2, isTreeWidgetClick):
        table = self.attributeView.attributeTable
        table.insertRow(table.rowCount())
        # set column 0 value
        table.setItem(table.rowCount() - 1, 0,
                                    QTableWidgetItem(value1))
        cell = table.item(table.rowCount() - 1, 0)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

        if value1 == "Name" or value1 == "Child Objects":
            pass
        else:
            cell.setToolTip(self.attributes[value1]["Description"])

        # set column 1 value
        table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(value2))
        cell = table.item(table.rowCount() - 1, 1)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)
        if not isTreeWidgetClick and value2 == None:
            cell.setBackground(QColor("indianred"))

    # if single clicking from the treeWidget, don't want to set the current sym
    # object
    def treeWidgetClicked(self, item, name):
        del self.state.selected_sym_objects[:]
        self.populateAttributes(item, name, True)

    # Populate the attribute table holding info for an objects params and children
    def populateAttributes(self, item, name, isTreeWidgetClick):
        table = self.attributeView.attributeTable
        table.clear()
        table.setRowCount(0)

        # If there is an object being viewed on the board display the name and
        #   connected objects as well
        if len(self.state.selected_sym_objects) == 1:
            cur_object = self.state.selected_sym_objects[0]
            self.addRow("Name", cur_object.name,
                        isTreeWidgetClick)
            self.addRow("Child Objects",
                        ", ".join(cur_object.connected_objects),
                        isTreeWidgetClick)

        if item:
            if item.parent() is None:
                return
            self.attributes = \
                self.catalog[item.parent().text(0)][item.text(0)]['params']
        else:
            # only load from param list if there is a sym object in the context
            if len(self.state.selected_sym_objects) == 1 or \
                self.state.selected_sym_objects[0].component_name == name:
                self.attributes = self.state.selected_sym_objects[0].instance_params
            else: # TODO: check when would this branch happen??
                print("filling in name branch")
                self.attributes = self.catalog[name]

        # display the param name and values
        for attribute in self.attributes.keys():
            self.addRow(attribute, str(self.attributes[attribute]["Value"]),
                                                    isTreeWidgetClick)

    # This function populates the tree view with sym-objects
    def populate(self):
        # Go through every inheritable sym-object
        for item in sorted(self.catalog.keys()):
            tree_item = QTreeWidgetItem([item])
            # Go through every specialized sym-object
            for sub_item in sorted(self.catalog[item].keys()):
                tree_item.addChild(QTreeWidgetItem([sub_item]))
            self.catalogView.treeWidget.addTopLevelItem(tree_item)

    # TODO still need this function to get description of parametrs
    def populateDescription(self, item):
        info = ""
        info += self.attributes[item.text()]["Description"]
        info += "\n"
        info += "Type: " + self.attributes[item.text()]["Type"]
        if self.attributes[item.text()]["Default"] is not None:
            info += "\n" + "Default Value: " + \
                    self.attributes[item.text()]["Default"]
        self.label.setText(info)

    # when user tries to exit, check if changes need to be saved before closing
    def closeEvent(self, event):
        if not self.state.mostRecentSaved:
            self.dialog = saveChangesDialog("closing")
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
