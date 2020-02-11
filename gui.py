try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

from graphic_field_scene_class import *
from graphic_system_item_class import *
from graphic_drag_label_class import *
from lineDrawer import *

import sys, random

class FieldWindow(QMainWindow):
    """this class creates a main window to observe the growth of a simulated field"""

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("gem5")


        #self.setCentralWidget(self.lines)


        #create toolbars
        self.tool_bar = QToolBar()

        #create toolbar labels
        self.System_label = SystemLabel()
        self.CPU_label = ComponentLabel("CPU")
        self.Cache_label = ComponentLabel("Cache")
        self.Membus_label = ComponentLabel("Membus")

        #add labels to toolbars
        self.tool_bar.addWidget(self.System_label)
        self.tool_bar.addWidget(self.CPU_label)
        self.tool_bar.addWidget(self.Cache_label)
        self.tool_bar.addWidget(self.Membus_label)


        #add toolbars to window
        self.addToolBar(self.tool_bar)

        self.addToolBar(Qt.LeftToolBarArea, self.tool_bar)

        self.field_graphics_view = QGraphicsView()
        self.scene = FieldGraphicsScene(1,5)



        self.lines = LineDrawer()
        self.proxy = self.scene.addWidget(self.lines)
        self.proxy.setWidget(self.lines)

        self.field_graphics_view.setScene(self.scene)


        self.field_graphics_view.setSceneRect(0,0,700,1200)
        self.field_graphics_view.setHorizontalScrollBarPolicy(1)
        self.field_graphics_view.setVerticalScrollBarPolicy(1)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.field_graphics_view)

        self.main = QWidget()

        self.main.setLayout(self.layout)
        self.setCentralWidget(self.main)


    def closeEvent(self, event):
        sys.exit()

def main():
    field_simulation = QApplication(sys.argv) #create new application
    field_window = FieldWindow() #create new instance of main window
    field_window.show() #make instance visible
    field_window.raise_() #raise instance to top of window stack

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)
    sys.exit(field_simulation.exec_()) #monitor application for events

if __name__ == "__main__":
    main()
