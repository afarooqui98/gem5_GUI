# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'catalog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
import json
import os


gem5_path = "/home/parallels/gem5"

class Ui_MainWindow(object):

    def __init__(self, catalog):
        self.catalog = catalog

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
        self.label.setFrameStyle(QtWidgets.QFrame.Panel |
            QtWidgets.QFrame.Sunken)
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
        match_items = self.treeWidget.findItems(search_string,
            QtCore.Qt.MatchContains)

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
            info += "\n" + "Default Value: " +
                self.attributes[item.text()]["Default"]
        self.label.setText(info)


def get_obj_lists():
    obj_tree = {}

    test_objects = ['BaseXBar', 'BranchPredictor', 'BaseCPU', 'BasePrefetcher',
        'IndirectPredictor', 'BaseCache', 'DRAMCtrl', 'Root', 'SimpleObject',
        'HelloObject', 'GoodbyeObject']

    for i in range(len(test_objects)):
        name = test_objects[i]
        obj_list = ObjectList.ObjectList(getattr(m5.objects, name, None))
        sub_objs = {}
        for sub_obj in obj_list._sub_classes.keys():
            param_dict = {}
            for pname, param in obj_list._sub_classes[sub_obj]._params.items():
                param_attr = {}
                param_attr["Description"] = param.desc
                param_attr["Type"] = param.ptype_str
                if hasattr(param, 'default'):

                    param_attr["Default"] = str(param.default)
                    param_attr["Value"] = str(param.default)
                else:
                    param_attr["Default"] = None
                    param_attr["Value"] = None
                param_dict[pname] = param_attr
            sub_objs[sub_obj] = param_dict

        obj_tree[name] = sub_objs
    return obj_tree


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    catalog = json.load(open('result.json'))

    ui = Ui_MainWindow(catalog)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__m5_main__":
    import sys
    sys.path.append('/home/parallels/gem5/configs')
    import m5.objects
    from common import ObjectList

    #mem_list = ObjectList.mem_list
    #mem_list.print()
    obj_tree = get_obj_lists()

    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(obj_tree)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
