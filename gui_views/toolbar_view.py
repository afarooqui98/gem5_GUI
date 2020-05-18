import sys
import random
import copy
import json
import logging

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from dialogs import *
from graphic_scene import *
from gui_views import state
from m5_calls import *

class ToolBarView():
    def __init__(self, layout, state, window):
        """set up the UI and connect button to its function"""
        self.state = state

        # Create toolbar and add a button to it
        self.toolbar = window.addToolBar("tools")
        self.drawWire = QAction(QIcon("images/draw_wire.png"), "draw wire",
                                window)
        self.drawWire.setShortcut("Ctrl+W")
        self.drawWire.triggered.connect(self.wireButtonPressed)

        # Connect the button to its associated function
        self.toolbar.addAction(self.drawWire)
        self.toolbar.setMouseTracking(True)
        self.toolbar.setCursor(QCursor(Qt.OpenHandCursor))


    def wireButtonPressed(self):
        """changes gui state to allow for wire drawing and
            disable object dragging"""
        # objects should not be movable or selectable
        self.state.dragState = not self.state.dragState
        self.state.selectState = not self.state.selectState
        self.state.drawWireState = not self.state.drawWireState
        self.state.setSymObjectFlags()

        # update cursor type immediately
        pos = QCursor.pos()
        QCursor.setPos(0, 0)
        QCursor.setPos(pos)

        # set the cursor type and button image based on wire state
        if self.state.drawWireState:
            QGuiApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
            self.drawWire.setIcon(QIcon("images/wire_pressed.png"))
        else:
            QGuiApplication.restoreOverrideCursor()
            self.drawWire.setIcon(QIcon("images/draw_wire.png"))
            self.state.lineDrawer.pos1 = None

        # update connections
        self.state.lineDrawer.update()
