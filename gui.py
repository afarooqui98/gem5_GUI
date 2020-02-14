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
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.wire_button = QPushButton("draw wire")
        self.gridLayout.addWidget(self.wire_button, 0, 0, 1, 1)
        self.save_button = QPushButton("save")
        self.gridLayout.addWidget(self.save_button, 0, 1, 1, 1)
        self.treeWidget = QTreeWidget()
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Name")
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 2)
        self.attributeList = QListWidget()
        self.attributeList.setObjectName("attributeList")
        self.gridLayout.addWidget(self.attributeList, 2, 0, 1, 2)

        self.label = QLabel()
        self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setScaledContents(True)
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

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
        self.treeWidget.itemClicked.connect(self.populateAttributes)
        self.treeWidget.itemDoubleClicked.connect(self.doubleClickEvent)
        self.attributeList.itemClicked.connect(self.populateDescription)
        self.wire_button.clicked.connect(wire_button_pressed)
        self.save_button.clicked.connect(save_button_pressed)

    def closeEvent(self, event):
        sys.exit()

    def doubleClickEvent(self, item):
        config.scene._visualise_graphic_item_center("component", item.text(0))

    def populateAttributes(self, item, column):
        self.attributeList.clear()
        self.attributes = self.catalog[item.text(0)]
        for attribute in self.attributes.keys():
            self.attributeList.addItem(attribute)


    def populate(self):
        for item in self.catalog.keys():
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
    field_window.show() #make instance visible
    field_window.raise_() #raise instance to top of window stack
    field_simulation.exec_() #monitor application for events
    field_simulation.quit()


if __name__ == "__main__":
    main()
