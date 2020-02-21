try:
    from PyQt4.QtGui import *
except:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *

from field_class import *
from graphic_system_item_class import *
from lineDrawer import *
from PyQt5 import QtCore
import config


class SymObject(QGraphicsItemGroup):

    def __init__(self, x, y, width, height, scene, component_name, name, loadingFromFile):
        super(SymObject, self).__init__()
        self.connected_objects = "" #TODO: at export, this string will become a list
        self.parameters = {}
        self.isMoving = False

        #initializing to (0, 0) so that future positions are relative to (0, 0)
        rect = QGraphicsRectItem(0, 0, width, height)

        self.x = scene.width() / 2 - width
        self.y = scene.height() / 2 - height
        self.width = width
        self.height = height
        self.component_name = component_name
        self.name = name
        self.to_export = 1
        self.scene = scene

        text = QGraphicsTextItem(component_name)
        text.setPos(rect.boundingRect().center() - text.boundingRect().center())

        self.deleteButton = QGraphicsTextItem('X')
        self.deleteButton.setPos(rect.boundingRect().topRight() - self.deleteButton.boundingRect().topRight())
        self.deleteButton.hide()

        port1 = QGraphicsEllipseItem(width/2 - config.port_size/2, height,
                                        config.port_size, config.port_size)
        port1.setBrush(QColor("Black"))

        port2 = QGraphicsEllipseItem(width/2 - config.port_size/2,
                        -config.port_size, config.port_size, config.port_size)
        port2.setBrush(QColor("Black"))

        self.addToGroup(rect)
        self.addToGroup(text)
        self.addToGroup(port1)
        self.addToGroup(port2)
        self.addToGroup(self.deleteButton)
        self.setAcceptDrops(True)

        if loadingFromFile:
            self.x = x
            self.y = y
            self.setPos(x, y)
            config.coord_map[(self.x, self.y)] = self.name
            return

        self.setPos(scene.width()/2 - width, scene.height()/2 - height)

        for key in config.sym_objects:
            item = config.sym_objects[key]
            if self.doOverlap(self.pos().x(), self.pos().y(), self.pos().x() +
            self.width, self.pos().y() + self.height, item.x, item.y, item.x +
            item.width, item.y + item.height):
                self.setPos(item.x + item.width + 10, item.y + item.height + 10)
                #del config.coord_map[(self.x, self.y)]
                self.x = self.pos().x()
                self.y = self.pos().y()
                config.coord_map[(self.x, self.y)] = self.name

        self.x = self.pos().x()
        self.y = self.pos().y()
        config.coord_map[(self.x, self.y)] = self.name


    #register mouse press events
    def mousePressEvent(self, event):
        super(SymObject, self).mousePressEvent(event)

        config.current_sym_object.deleteButton.hide()
        self.deleteButton.show()

        deletePressed = self.deleteButtonPressed()
        if deletePressed:
            print("Deleting", self.name)
            self.delete()
            return

        config.current_sym_object = self
        config.mainWindow.populateAttributes(None, self.component_name, False)

    def delete(self):
        config.scene.removeItem(self)
        config.current_sym_object = None
        del config.coord_map[(self.x, self.y)]
        del config.sym_objects[self.name]

    # when mouse is release on object, update its position including the case
    # where it overlaps
    def mouseReleaseEvent(self, event):
        super(SymObject, self).mouseReleaseEvent(event)

        if self.x == self.pos().x() and self.y == self.pos().y():
            return

        #iterate through all sym objects on the screen and check if the object's
        # current position overlaps with any of them
        for key in config.sym_objects:
            item = config.sym_objects[key]
            if self != item:
                if self.doOverlap(self.pos().x(), self.pos().y(), self.pos().x()
                 + self.width, self.pos().y() + self.height, item.x, item.y,
                 item.x + item.width, item.y + item.height):
                    self.setPos(self.x, self.y)
                    return

        # update the object's position parameters
        del config.coord_map[(self.x, self.y)]
        self.x = self.pos().x()
        self.y = self.pos().y()
        config.coord_map[(self.x, self.y)] = self.name

    def deleteButtonPressed(self):
        click_x, click_y = self.getClickCoords(self.deleteButton)
        click_x = click_x - self.x
        click_y = click_y - self.y

        deleteButton_x = self.deleteButton.pos().x()
        deleteButton_y = self.deleteButton.pos().y()

        if (abs(click_x - deleteButton_x) <= 5) and (abs(click_y - deleteButton_y) <= 5):
            return True

        return False

    def getClickCoords(self,item):
        cursor_position = QCursor.pos() #global cursor position
        current_view = config.scene.views()[0]
        scene_position = current_view.mapFromGlobal(cursor_position)

        width = item.boundingRect().width()
        height = item.boundingRect().height()

        drop_x = scene_position.x()
        drop_y = scene_position.y()

        return drop_x, drop_y

    def doOverlap(self, l1_x, l1_y, r1_x, r1_y, l2_x, l2_y, r2_x, r2_y):
        notoverlap = l1_x > r2_x or l2_x > r1_x or l1_y > r2_y or l2_y > r1_y
        return not notoverlap
