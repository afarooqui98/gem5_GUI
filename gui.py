
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphic_scene import *
from gui_views.catalog_view import *
from gui_views.button_view import *
from gui_views.catalog_view import *
from gui_views.attribute_view import *
from gui_views.config import *

import sys, random
import copy
import json

class MainWindow(QMainWindow):
    """this class creates the main window"""
    catalog = json.load(open('result_new.json'))

    def __init__(self, catalog):
        super(MainWindow, self).__init__()
        self.setWindowTitle("gem5 GUI")
        self.main = QWidget()
        self.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout = QVBoxLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.buttonView = ButtonView(self.gridLayout) #add button view
        self.catalogView = CatalogView(self.gridLayout) #add catalog view
        self.attributeView = AttributeView(self.gridLayout) #add attributes

        self.field_graphics_view = QGraphicsView()
        config.scene = GraphicsScene()

        self.lines = LineDrawer()
        self.proxy = config.scene.addWidget(self.lines)
        self.proxy.setWidget(self.lines)

        self.field_graphics_view.setScene(config.scene)
        self.field_graphics_view.setSceneRect(0,0,700,600)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.gridLayout)
        self.layout.addWidget(self.field_graphics_view)

        self.main.setLayout(self.layout)
        self.setCentralWidget(self.main)

        # populate treeview
        self.populate()
        self.catalogView.treeWidget.itemClicked.connect(self.treeWidgetClicked)

    def closeEvent(self, event):
        sys.exit()

    def addRow(self, value1, value2, isTreeWidgetClick):
        table = self.AttributeView.attributeTable
        table.insertRow(self.attributeTable.rowCount())
        # set column 0 value
        table.setItem(self.attributeTable.rowCount() - 1, 0,
                                    QTableWidgetItem(value1))
        cell = table.item(table.rowCount() - 1, 0)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

        # set column 1 value
        table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(value2))
        cell = table.item(table.rowCount() - 1, 1)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)
        if not isTreeWidgetClick and value2 == None:
            cell.setBackground(QColor("indianred"))

    # if single clicking from the treeWidget, don't want to set the current sym
    # object
    def treeWidgetClicked(self, item, name):
        config.current_sym_object = None
        self.populateAttributes(item, name, True)

    def populateAttributes(self, item, name, isTreeWidgetClick):
        table = self.AttributeView.attributeTable
        table.clear()
        table.setRowCount(0)

        if config.current_sym_object != None:
            print(config.current_sym_object.component_name)
            self.addRow("Name", config.current_sym_object.name,
                        isTreeWidgetClick)
            self.addRow("Child Objects",
                        config.current_sym_object.connected_objects,
                        isTreeWidgetClick)

        if item:
            if item.parent() is None:
                return
            self.attributes = self.catalog[item.parent().text(0)][item.text(0)]
        else:
            # only load from param list if there is a sym object in the context
            if config.current_sym_object != None or \
                config.current_sym_object.component_name == name:
                print("filling in current sym obj branch")
                self.attributes = config.current_sym_object.parameters
            else: # TODO: check when would this branch happen??
                print("filling in name branch")
                self.attributes = self.catalog[name]

        for attribute in self.attributes.keys():
            self.addRow(attribute, self.attributes[attribute]["Value"],
                                                    isTreeWidgetClick)


    def populate(self):
        """
        This function populates the tree view with sym-objects
        """
        # Go through every inheritable sym-object
        for item in sorted(self.catalog.keys()):
            tree_item = QTreeWidgetItem([item])
            # Go through every specialized sym-object
            for sub_item in self.catalog[item].keys():
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

if __name__ == "__main__":
    gui_application = QApplication() #create new application
    catalog = json.load(open('result_new.json'))
    main_window = MainWindow(catalog) #create new instance of main window
    config.mainWindow = main_window
    main_window.show() #make instance visible
    main_window.raise_() #raise instance to top of window stack
    gui_application.exec_() #monitor application for events
    gui_application.quit()


if __name__ == "__m5_main__":
    import sys
    sys.path.append('configs')
    import m5.objects
    from common import ObjectList
    from m5_calls import get_obj_lists

    # use gem5 to get list of objects
    obj_tree = get_obj_lists()

    gui_application = QApplication() #create new application
    main_window = MainWindow(obj_tree) #create new instance of main window
    config.mainWindow = main_window
    main_window.show() #make instance visible
    main_window.raise_() #raise instance to top of window stack
    gui_application.exec_() #monitor application for events
    gui_application.quit()
