try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

from graphic_field_scene_class import *
from graphic_system_item_class import *
from graphic_drag_label_class import *
from wire_button import *

import sys, random
import config

class FieldWindow(QMainWindow):
    """this class creates a main window to observe the growth of a simulated field"""

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("gem5")

        #create toolbars
        self.tool_bar = QToolBar()

        self.wire_button = QPushButton("draw wire")
        self.wire_button.clicked.connect(wire_button_pressed)
        #create toolbar labels
        self.System_label = SystemLabel()
        self.CPU_label = ComponentLabel("CPU")
        self.Cache_label = ComponentLabel("Cache")
        self.Membus_label = ComponentLabel("Membus")

        #add labels to toolbars
        self.tool_bar.addWidget(self.wire_button)
        self.tool_bar.addWidget(self.System_label)
        self.tool_bar.addWidget(self.CPU_label)
        self.tool_bar.addWidget(self.Cache_label)
        self.tool_bar.addWidget(self.Membus_label)


        #add toolbars to window
        self.addToolBar(self.tool_bar)

        self.addToolBar(Qt.LeftToolBarArea, self.tool_bar)

        self.field_graphics_view = QGraphicsView()
        self.field_graphics_view.setScene(FieldGraphicsScene(1,5))

        self.field_graphics_view.setSceneRect(0,0,700,1200)
        self.field_graphics_view.setHorizontalScrollBarPolicy(1)
        self.field_graphics_view.setVerticalScrollBarPolicy(1)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.field_graphics_view)

        self.main = QWidget()

        self.main.setLayout(self.layout)
        self.setCentralWidget(self.main)
        #connections
        #self.field_automatic_grow_button.clicked.connect(self.automatically_grow)
        #self.field_manual_grow_button.clicked.connect(self.manually_grow)
        #self.field_report_button.clicked.connect(self.report)
    def closeEvent(self, event):
        sys.exit()

def main():
    field_simulation = QApplication(sys.argv) #create new application
    field_window = FieldWindow() #create new instance of main window
    field_window.show() #make instance visible
    field_window.raise_() #raise instance to top of window stack
    field_simulation.exec_() #monitor application for events
    field_simulation.quit()

if __name__ == "__main__":
    main()
