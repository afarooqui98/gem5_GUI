try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

from graphic_field_scene_class import *
from graphic_system_item_class import *
from graphic_drag_label_class import *

import sys, random
import copy
import config
from button import *
import json

class FieldWindow(QMainWindow):
    """this class creates the main window"""
    catalog = json.load(open('result_new.json'))

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("gem5")
        self.main = QWidget()
        self.setLayoutDirection(Qt.LeftToRight)

        #catalog start
        self.gridLayout = QVBoxLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.wire_button = QPushButton("draw wire")
        self.gridLayout.addWidget(self.wire_button)
        self.export_button = QPushButton("export")
        self.gridLayout.addWidget(self.export_button)

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
        config.scene = FieldGraphicsScene(1,5)

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

        self.populate() #populate treeview
        self.treeWidget.itemClicked.connect(self.treeWidgetClicked)
        self.treeWidget.itemDoubleClicked.connect(self.doubleClickEvent)
        self.edit.textChanged.connect(self.searchItem)
        self.attributeTable.itemDoubleClicked.connect(self.makeEditable)
        self.wire_button.clicked.connect(wire_button_pressed)
        self.export_button.clicked.connect(export_button_pressed)

    def closeEvent(self, event):
        sys.exit()

    #make tree view searchable
    def searchItem(self):
        """
        Searches treeview whenever a user types something in the search bar
        """
        # Get string in the search bar and use treeview's search fn
        search_string = self.edit.text()
        match_items = self.treeWidget.findItems(search_string, Qt.MatchContains | Qt.MatchRecursive)

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

    #this function feeds into the next one, after the cell is changed it will trigger
    def makeEditable(self, item):
        #set item to editable
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.attributeTable.itemChanged.connect(self.modifyFields)

    def addRow(self, value1, value2):
        self.attributeTable.insertRow(self.attributeTable.rowCount())
        #set column 0 value
        self.attributeTable.setItem(self.attributeTable.rowCount() - 1, 0, QTableWidgetItem(value1))
        cell = self.attributeTable.item(self.attributeTable.rowCount() - 1, 0)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

        #set column 1 value
        self.attributeTable.setItem(self.attributeTable.rowCount() - 1, 1, QTableWidgetItem(value2))
        cell = self.attributeTable.item(self.attributeTable.rowCount() - 1, 1)
        cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

    #this signal disconnects itself after finishing execution, since we only want to trigger it AFTER a double press
    def modifyFields(self, item):
        if config.current_sym_object == None or item == None:
            return

        #get attributes
        currentColumn = self.attributeTable.column(item)
        currentRow = self.attributeTable.row(item)
        currentAttribute = self.attributeTable.item(currentRow, currentColumn - 1).text()
        currentValue = item.text()

        #if the value is name or connected objects, set the param instead of the dict
        if currentAttribute == "Name":
            config.current_sym_object.name = currentValue
            current_x = config.current_sym_object.x
            current_y = config.current_sym_object.y
            current_name = config.current_sym_object.name
            if (current_x, current_y) in config.coord_map:
                del config.sym_objects[config.coord_map[(current_x, current_y)]]

            config.coord_map[(current_x, current_y)] = current_name
            config.sym_objects[current_name] = config.current_sym_object
        elif currentAttribute == "Connected Objects":
            config.current_sym_object.connected_objects = currentValue
            config.sym_objects[currentValue].to_export = 0
        else:
            config.current_sym_object.parameters[currentAttribute]["Value"] = currentValue

        #item no longer editable, disconnect
        self.attributeTable.itemChanged.disconnect(self.modifyFields)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)

    def doubleClickEvent(self, item):
        if item.parent() is None:
            return
        config.current_sym_object = config.scene._visualise_graphic_item_center("component", item.text(0))
        config.current_sym_object.parameters = copy.deepcopy(self.catalog[item.parent().text(0)][item.text(0)])

    def treeWidgetClicked(self, item, name): #if single clicking from the treeWidget, don't want to set the current sym object
        config.current_sym_object = None
        self.populateAttributes(item, name)

    def populateAttributes(self, item, name):
        self.attributeTable.clear()
        self.attributeTable.setRowCount(0)

        if config.current_sym_object != None:
            print(config.current_sym_object.component_name)
            self.addRow("Name", config.current_sym_object.name)
            self.addRow("Connected Objects", config.current_sym_object.connected_objects)

        if item:
            if item.parent() is None:
                return
            self.attributes = self.catalog[item.parent().text(0)][item.text(0)]
        else:
            if config.current_sym_object != None or config.current_sym_object.component_name == name: #only load from param list if there is a sym object in the context
                print("filling in current sym obj branch")
                self.attributes = config.current_sym_object.parameters
            else: #TODO: check when would this branch happen??
                print("filling in name branch")
                self.attributes = self.catalog[name]

        for attribute in self.attributes.keys():
            self.addRow(attribute, self.attributes[attribute]["Value"])


    def populate(self):
        for item in sorted(self.catalog.keys()):
            tree_item = QTreeWidgetItem([item])
            for sub_item in self.catalog[item].keys():
                tree_item.addChild(QTreeWidgetItem([sub_item]))
            self.treeWidget.addTopLevelItem(tree_item)

    def populateDescription(self, item):
        info = ""
        info += self.attributes[item.text()]["Description"]
        info += "\n"
        info += "Type: " + self.attributes[item.text()]["Type"]
        if self.attributes[item.text()]["Default"] is not None:
            info += "\n" + "Default Value: " + self.attributes[item.text()]["Default"]
        self.label.setText(info)

def main():
    field_simulation = QApplication(sys.argv) #create new application
    field_window = FieldWindow() #create new instance of main window
    config.mainWindow = field_window
    field_window.show() #make instance visible
    field_window.raise_() #raise instance to top of window stack
    field_simulation.exec_() #monitor application for events
    field_simulation.quit()


if __name__ == "__main__":
    main()
