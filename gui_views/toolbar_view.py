from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from dialogs import *
from graphic_scene import *
from gui_views import state
from m5_calls import *

import sys
import random
import copy
import json
import logging

class ToolBarView():
    def __init__(self, layout, state, window):
        """set up the UI and connect button to its function"""
        self.state = state

        # Create toolbar and add a button to it
        self.toolbar = window.addToolBar("tools")
        self.draw_wire = QAction(QIcon("images/draw_wire.png"), "draw wire",
                                window)
        self.draw_wire.setShortcut("Ctrl+W")
        self.draw_wire.triggered.connect(self.wire_button_pressed)

        # Connect the button to its associated function
        self.toolbar.addAction(self.draw_wire)
        self.toolbar.setMouseTracking(True)
        self.toolbar.setCursor(QCursor(Qt.OpenHandCursor))


    def wire_button_pressed(self):
        """changes gui state to allow for wire drawing and
            disable object dragging"""
        # objects should not be movable or selectable
        self.state.drag_state = not self.state.drag_state
        self.state.select_state = not self.state.select_state
        self.state.draw_wire_state = not self.state.draw_wire_state
        self.state.setSymObjectFlags()

        # update cursor type immediately
        pos = QCursor.pos()
        QCursor.setPos(0, 0)
        QCursor.setPos(pos)

        # set the cursor type and button image based on wire state
        if self.state.draw_wire_state:
            QGuiApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
            self.draw_wire.setIcon(QIcon("images/wire_pressed.png"))
        else:
            QGuiApplication.restoreOverrideCursor()
            self.draw_wire.setIcon(QIcon("images/draw_wire.png"))
            self.state.line_drawer.pos1 = None

        # update connections
        self.state.line_drawer.update()
