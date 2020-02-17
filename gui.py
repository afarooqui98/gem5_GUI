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
import config
from button import *
import json

class FieldWindow(QMainWindow):
    """this class creates the main window"""
    catalog = json.load(open('result.json'))

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
        self.attributeTable.itemDoubleClicked.connect(self.makeEditable)
        self.wire_button.clicked.connect(wire_button_pressed)
        self.export_button.clicked.connect(export_button_pressed)
    def closeEvent(self, event):
        sys.exit()

    #this function feeds into the next one, after the cell is changed it will trigger
    def makeEditable(self, item):
        #set item to editable
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.attributeTable.itemChanged.connect(self.modifyCurrentSym_object)

    #this signal disconnects itself after finishing execution, since we only want to trigger it AFTER a double press
    def modifyCurrentSym_object(self, item):
        if config.current_sym_object == None or item == None:
            return
        print(config.current_sym_object.parameters)
        print(config.sym_objects)
        currentColumn = self.attributeTable.column(item)
        currentRow = self.attributeTable.row(item)
        currentAttribute = self.attributeTable.item(currentRow, currentColumn - 1).text()
        currentValue = item.text()
        config.current_sym_object.parameters[currentAttribute]["Default"] = currentValue

        #item no longer editable, disconnect
        self.attributeTable.itemChanged.disconnect(self.modifyCurrentSym_object)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        
    def doubleClickEvent(self, item):
        config.scene._visualise_graphic_item_center("component", item.text(0))
    
    def treeWidgetClicked(self, item, name): #if single clicking from the treeWidget, don't want to set the current sym object
        config.current_sym_object = None
        self.populateAttributes(item, name)

    def populateAttributes(self, item, name):
        self.attributeList.clear()
        if item:
            self.attributes = self.catalog[item.text(0)]
        else:
            self.attributes = self.catalog[name]

        for attribute in self.attributes.keys():
            self.attributeTable.insertRow(self.attributeTable.rowCount())

            #set column 0 value
            self.attributeTable.setItem(self.attributeTable.rowCount() - 1, 0, QTableWidgetItem(attribute))
            cell = self.attributeTable.item(self.attributeTable.rowCount() - 1, 0)
            cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

            #set column 1 value
            self.attributeTable.setItem(self.attributeTable.rowCount() - 1, 1, QTableWidgetItem(self.attributes[attribute]["Default"]))
            cell = self.attributeTable.item(self.attributeTable.rowCount() - 1, 1)
            cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)

    def populate(self):
        for item in sorted(self.catalog.keys()):
            self.treeWidget.addTopLevelItem(QTreeWidgetItem([item]))

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
