# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'catalog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os


gem5_path = "/home/parallels/gem5"
gem5_run_option = "build/X86/gem5.opt"

def get_catalog():
    script = os.getcwd() + "/../m5_calls/get_catalog.py"

    os.system(gem5_path + "/" + gem5_run_option + " " + script)
    m5_catalog = json.load(open('result.json'))
    return m5_catalog



class Ui_MainWindow(object):
    #catalog = json.load(open('result.json'))
    catalog = get_catalog()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.edit = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.edit, 0, 0, 1, 1)

        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Name")
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 1)

        self.attributeList = QtWidgets.QListWidget(self.centralwidget)
        self.attributeList.setObjectName("attributeList")
        self.gridLayout.addWidget(self.attributeList, 2, 0, 1, 1)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        #self.label.setText("first line\nsecond line")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)


        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.populate() #populate treeview

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.treeWidget.itemClicked.connect(self.populateAttributes)
        self.attributeList.itemClicked.connect(self.populateDescription)
        self.edit.textChanged.connect(self.searchItem)


    def searchItem(self):
        search_string = self.edit.text()
        match_items = self.treeWidget.findItems(search_string, QtCore.Qt.MatchContains)

        root = self.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setHidden(item not in match_items)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def populateAttributes(self, item, column):
        if item.parent() is None:
            return

        self.attributeList.clear()
        self.attributes = self.catalog[item.parent().text(0)][item.text(0)]
        for attribute in self.attributes.keys():
            self.attributeList.addItem(attribute)


    def populate(self):
        for item in sorted(self.catalog.keys()):
            tree_item = QtWidgets.QTreeWidgetItem([item])
            for sub_item in self.catalog[item].keys():
                tree_item.addChild(QtWidgets.QTreeWidgetItem([sub_item]))
            self.treeWidget.addTopLevelItem(tree_item)


    def populateDescription(self, item):
        info = ""
        info += self.attributes[item.text()]["Description"]
        info += "\n"
        info += "Type: " + self.attributes[item.text()]["Type"]
        if self.attributes[item.text()]["Default"] is not None:
            info += "\n" + "Default Value: " + self.attributes[item.text()]["Default"]
        self.label.setText(info)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
