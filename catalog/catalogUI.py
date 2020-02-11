# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'catalog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class TreeObject(object):
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

def populate():
    objectList = []
    for i in range(6):
        treeObj = TreeObject("thing" + str(i), ["attr1", "attr2", "attr3", "attr4"])
        objectList.append(treeObj)
    return objectList

class Ui_MainWindow(object):
    FROM, SUBJECT, DATE = range(3)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.catalogView = QtWidgets.QTreeView(self.centralwidget)
        self.catalogView.setObjectName("catalogView")
        self.gridLayout.addWidget(self.catalogView, 0, 0, 1, 1)
        self.attributeView = QtWidgets.QListView(self.centralwidget)
        self.attributeView.setObjectName("attributeView")
        self.gridLayout.addWidget(self.attributeView, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #populate catalogview
        model = self.fillCatalog(populate())
        self.catalogView.setModel(model)

        #signal for treeview selection
        self.catalogView.selectionModel().selectionChanged.connect(self.listPopulate)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def listPopulate(self):
        #populate
        model = QtGui.QStandardItemModel()
        self.attributeView.setModel(model)
        entries = ['one','two', 'three']
        for i in entries:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)

    def fillCatalog(self, objectList):
        model = QtGui.QStandardItemModel(0, 3, self.centralwidget)
        model.setHeaderData(self.FROM, QtCore.Qt.Horizontal, "From")
        model.setHeaderData(self.SUBJECT, QtCore.Qt.Horizontal, "Subject")
        model.setHeaderData(self.DATE, QtCore.Qt.Horizontal, "Date")

        model.insertRow(0)
        model.setData(model.index(0, self.FROM), 'service@github.com')
        model.setData(model.index(0, self.SUBJECT), 'test2')
        model.setData(model.index(0, self.DATE), 'test3')
        # model = QtGui.QStandardItemModel()
        # model.clear()
        # for obj in objectList:
        #     print("inserting" + obj.name)
        #     model.insertRow(0)
        #     model.setData(model.index(0, 0), obj.name)
        #     model.addItems(model, obj.name)
        #
        # model.setHorizontalHeaderLabels(['Name'])
        return model


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
