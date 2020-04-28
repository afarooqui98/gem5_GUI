from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *
from dialogs import *

import sys, random
import copy
from gui_views import state
import json
import logging


from m5_calls import *

class ToolBarView():
    def __init__(self, layout, state, window):
        self.state = state
        self.toolbar = window.addToolBar("tools")
        self.draw_wire = QAction(QIcon("images/draw_wire.png"), "draw wire", window)
        self.draw_wire.setShortcut("Ctrl+W")
        self.draw_wire.triggered.connect(self.wire_button_pressed)
        self.toolbar.addAction(self.draw_wire)
        self.toolbar.setMouseTracking(True)
        self.toolbar.setCursor(QCursor(Qt.OpenHandCursor))


    def wire_button_pressed(self):
        """changes gui state to allow for wire drawing and
            disable object dragging"""
        self.state.drag_state = not self.state.drag_state
        self.state.draw_wire_state = not self.state.draw_wire_state
        self.state.setDragState()
        #update cursor type immediately
        pos = QCursor.pos()
        QCursor.setPos(0, 0)
        QCursor.setPos(pos)
        if self.state.draw_wire_state:
            self.state.line_drawer.setCursor(QCursor(Qt.CrossCursor))
            self.draw_wire.setIcon(QIcon("images/wire_pressed.png"))
        else:
            self.state.line_drawer.setCursor(QCursor(Qt.ArrowCursor))
            self.draw_wire.setIcon(QIcon("images/draw_wire.png"))
        self.state.line_drawer.update()
