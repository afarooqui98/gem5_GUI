
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphic_scene import *

import sys, random
import copy
import config
from button import *
import json

class MainWindow(QMainWindow):
    """this class creates the main window"""

    def __init__(self, catalog):
        super(MainWindow, self).__init__()
        self.catalog = catalog
        self.setWindowTitle("gem5 GUI")
        self.main = QWidget()
        self.setLayoutDirection(Qt.LeftToRight)

        # catalog start
        self.gridLayout = QVBoxLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.wire_button = QPushButton("draw wire")
        self.gridLayout.addWidget(self.wire_button)
        self.export_button = QPushButton("export")
        self.gridLayout.addWidget(self.export_button)
        self.saveUI_button = QPushButton("Save Configuration")
        self.gridLayout.addWidget(self.saveUI_button)
        self.openUI_button = QPushButton("Open Configuration")
        self.gridLayout.addWidget(self.openUI_button)

        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Search for an object here!")
        self.gridLayout.addWidget(self.edit)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Name")
        self.gridLayout.addWidget(self.treeWidget)

        self.attributeLayout = QHBoxLayout()
        self.attributeTable = QTableWidget(0,2)
        self.attributeTable.setObjectName("attributeTable")
        self.attributeTable.verticalHeader().setVisible(False)
        self.attributeTable.horizontalHeader().setVisible(False)
        header = self.attributeTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.attributeLayout.addWidget(self.attributeTable)

        self.gridLayout.addLayout(self.attributeLayout)


        self.label = QLabel()
        self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setScaledContents(True)
        self.gridLayout.addWidget(self.label)

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
        self.treeWidget.itemClicked.connect(self.treeWidgetClicked)
        self.treeWidget.itemDoubleClicked.connect(self.doubleClickEvent)
        self.edit.textChanged.connect(self.searchItem)
        self.attributeTable.itemDoubleClicked.connect(self.makeEditable)
        self.wire_button.clicked.connect(wire_button_pressed)
        self.export_button.clicked.connect(export_button_pressed)
        self.saveUI_button.clicked.connect(saveUI_button_pressed)
        self.openUI_button.clicked.connect(openUI_button_pressed)

    def closeEvent(self, event):
        sys.exit()

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
                    not_found = not_found or (grand_item in match_items)
                # hide and expand top-level item based on if sub-level item
                #   is a match
                item.setHidden(not not_found)
                item.setExpanded(not_found)

    # this function feeds into the next one, after the cell is changed it will
    # trigger
    def makeEditable(self, item):
        # set item to editable
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.attributeTable.itemChanged.connect(self.modifyFields)

    def addRow(self, value1, value2, isTreeWidgetClick):
        self.attributeTable.insertRow(self.attributeTable.rowCount())
        # set column 0 value
        self.attributeTable.setItem(self.attributeTable.rowCount() - 1, 0,
                                    QTableWidgetItem(value1))
        cell = self.attributeTable.item(self.attributeTable.rowCount() - 1, 0)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

        # set column 1 value
        self.attributeTable.setItem(self.attributeTable.rowCount() - 1, 1,
                                    QTableWidgetItem(value2))
        cell = self.attributeTable.item(self.attributeTable.rowCount() - 1, 1)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)
        if not isTreeWidgetClick and value2 == None:
            cell.setBackground(QColor("indianred"))

    # this signal disconnects itself after finishing execution, since we only
    # want to trigger it AFTER a double press
    def modifyFields(self, item):
        if config.current_sym_object == None or not item:
            return

        # get attributes
        currentColumn = self.attributeTable.column(item)
        currentRow = self.attributeTable.row(item)
        currentAttribute = self.attributeTable.item(currentRow,
                                                    currentColumn - 1).text()
        currentValue = item.text()

        # if the value is name or connected objects, set the param instead of
        # the dict
        if currentAttribute == "Name":
            config.current_sym_object.name = currentValue
            current_x = config.current_sym_object.x
            current_y = config.current_sym_object.y
            current_name = config.current_sym_object.name
            if (current_x, current_y) in config.coord_map:
                del config.sym_objects[config.coord_map[(current_x, current_y)]]

            config.coord_map[(current_x, current_y)] = current_name
            config.sym_objects[current_name] = config.current_sym_object
        elif currentAttribute == "Child Objects":
            config.current_sym_object.connected_objects = currentValue
            config.sym_objects[currentValue].to_export = 0
            config.line_drawer.connectSubObject(config.current_sym_object.name,
                                                currentValue)
        else:
            config.current_sym_object.parameters[currentAttribute]["Value"] = \
                                                                    currentValue

        # item no longer editable, disconnect
        self.attributeTable.itemChanged.disconnect(self.modifyFields)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        if currentValue:
            item.setBackground(QColor("white"))

    def doubleClickEvent(self, item):
        if item.parent() is None:
            return

        name, ok = QInputDialog.getText(self, "Alert", "New SimObject name:")
        if not ok:
            return

        config.current_sym_object = config.scene. \
                addObjectToScene("component", item.text(0), name)
        config.current_sym_object.parameters = copy.deepcopy(
                            self.catalog[item.parent().text(0)][item.text(0)])

    # if single clicking from the treeWidget, don't want to set the current sym
    # object
    def treeWidgetClicked(self, item, name):
        config.current_sym_object = None
        self.populateAttributes(item, name, True)

    def populateAttributes(self, item, name, isTreeWidgetClick):
        self.attributeTable.clear()
        self.attributeTable.setRowCount(0)

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
            self.treeWidget.addTopLevelItem(tree_item)

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
