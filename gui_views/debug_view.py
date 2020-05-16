from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphic_scene import *
from m5_calls import *

import sys, random
import copy
from gui_views import state
import json
import logging

class DebugWidget(QWidget):
    """Displays options for development and allows enabling of these options"""
    def __init__(self, state):
        super(DebugWidget, self).__init__()
        self.state = state
        self.flags = get_debug_flags()
        self.debug_layout = QVBoxLayout()
        self.debug_statements = True

        # Add check box to redirect debug statements to log file
        self.file_box = QCheckBox("Log to File")
        self.file_box.setChecked(True)
        self.file_box.stateChanged.connect(lambda:self.btnState(self.file_box))

        # Add input to edit name of log file
        self.logfile_edit = QLineEdit()
        self.logfile_edit.setPlaceholderText("Enter filename")
        self.logfile_edit.setText("debug.log")
        self.logfile_edit.setFixedWidth(150)
        self.logfile_edit.editingFinished.connect(self.switch_debug_output)

        # Add check box to redirect debug statements to stdout
        self.stdout_box = QCheckBox("Log to Stdout")
        self.stdout_box.toggled.connect(lambda:self.btnState(self.stdout_box))

        # search bar for the debug flags
        self.flag_search = QLineEdit()
        self.flag_search.setPlaceholderText("Search for a debug flag here!")
        self.flag_search.setFixedWidth(250)
        self.flag_search.textChanged.connect(self.searchFlag)

        self.flag_list = self.createFlagList()
        self.flag_list.resize(250, 250)

        # Add widgets to layout
        self.debug_layout.addWidget(self.file_box)
        self.debug_layout.addWidget(self.logfile_edit)
        self.debug_layout.addWidget(self.stdout_box)
        self.debug_layout.addWidget(self.flag_search)
        self.debug_layout.addWidget(self.flag_list, 50)
        self.debug_layout.addStretch(5)
        self.debug_layout.setSpacing(10)

        # Add debug layout to the main layout
        self.setLayout(self.debug_layout)
        self.switch_debug_output()


    def searchFlag(self, text):
        """ Search the list widget for flags that match the text"""
        for row in range(self.flag_list.count()):
            flag = self.flag_list.item(row)
            if text:
                flag.setHidden(not text in flag.text())
            else:
                flag.setHidden(False)


    def switch_debug_output(self):
        """ This handler switches between stdout and a file for debug msgs"""
        # Get rid of current stream
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        if self.debug_statements:
            # redirect debug msgs to file
            logfile = self.logfile_edit.text()
            if '.' not in logfile:
                logfile += '.log'

            logging.basicConfig(filename=logfile, filemode='w', level= \
                logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
        else:
            # redirect debug msgs to terminal
            logging.basicConfig(level=logging.DEBUG)


    def btnState(self, box):
        """ If file_box or stdout_box are checked the other shld be unchecked"""
        if box.text() == "Log to File":
            if box.isChecked():
                self.stdout_box.setChecked(False)
                # should not edit filename
                self.logfile_edit.setReadOnly(False)
                self.debug_statements = True
                self.switch_debug_output()

        if box.text() == "Log to Stdout":
            if box.isChecked():
                self.file_box.setChecked(False)
                self.logfile_edit.setReadOnly(True)
                self.debug_statements = False
                self.switch_debug_output()

    def createFlagList(self):
        """ Create list widget with all the debug flags"""
        flag_list = QListWidget()
        for key in self.flags.keys():
            flag_item = QListWidgetItem()
            flag_item.setText(key)
            flag_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            flag_item.setCheckState(Qt.Unchecked)
            flag_list.addItem(flag_item)

        flag_list.itemClicked.connect(self.flagEnable)
        return flag_list

    def flagEnable(self, item):
        """ Event handler to enable or disable debug flags """
        if item.checkState() == Qt.Checked:
            logging.debug('"%s" Checked' % item.text())
            self.flags[item.text()].enable()
        elif item.checkState() == Qt.Unchecked:
            logging.debug('"%s" Unchecked' % item.text())
            self.flags[item.text()].disable()
        else:
            logging.debug('"%s" Clicked' % item.text())
