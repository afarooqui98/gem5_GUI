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

    def __init__(self, x, y, width, height, scene, component_name):
        super(SymObject, self).__init__()
        self.connected_objects = []
        self.isMoving = False

        #initializing to (0, 0) so that future positions are relative to (0, 0)
        rect = QGraphicsRectItem(0, 0, width, height)

        self.x = scene.width() / 2 - width
        self.y = scene.height() / 2 - height
        self.width = width
        self.height = height
        self.component_name = component_name

        text = QGraphicsTextItem(component_name)
        text.setPos(rect.boundingRect().center() - text.boundingRect().center())

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

        self.setPos(scene.width()/2 - width, scene.height()/2 - height)

        for key in config.sym_objects:
            item = config.sym_objects[key]
            if self.doOverlap(self.pos().x(), self.pos().y(), self.pos().x() +
            self.width, self.pos().y() + self.height, item.x, item.y, item.x +
            item.width, item.y + item.height):
                self.setPos(item.x + item.width + 10, item.y + item.height + 10)
                self.x = self.pos().x()
                self.y = self.pos().y()

        self.setAcceptDrops(True)

    #register mouse press events
    def mousePressEvent(self, event):
        super(SymObject, self).mousePressEvent(event)
        config.current_sym_object = self
        config.mainWindow.populateAttributes(None, self.component_name)

    # when mouse is release on object, update its position including the case
    # where it overlaps
    def mouseReleaseEvent(self, event):
        super(SymObject, self).mouseReleaseEvent(event)
        #iterate through all sym objects on the screen and check if the object's
        # current position overlaps with any of them
        for key in config.sym_objects:
            item = config.sym_objects[key]
            if self != item:
                if self.doOverlap(self.pos().x(), self.pos().y(), self.pos().x()
                 + self.width, self.pos().y() + self.height, item.x, item.y,
                 item.x + item.width, item.y + item.height):
                    self.setPos(self.x, self.y)

        # update the object's position parameters
        self.x = self.pos().x()
        self.y = self.pos().y()

    def doOverlap(self, l1_x, l1_y, r1_x, r1_y, l2_x, l2_y, r2_x, r2_y):
        notoverlap = l1_x > r2_x or l2_x > r1_x or l1_y > r2_y or l2_y > r1_y
        return not notoverlap
