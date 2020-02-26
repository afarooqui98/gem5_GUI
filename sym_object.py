from lineDrawer import *
from PySide2 import QtCore
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from gui_views import config


class SymObject(QGraphicsItemGroup):

    def __init__(self, x, y, width, height, scene, component_name, name,
                    loadingFromFile):
        super(SymObject, self).__init__()
        #TODO: at export, this string will become a list
        self.connected_objects = ""
        self.parameters = {}
        self.connections = {}
        self.isMoving = False

        # set initial attributes for new symobject
        self.x = scene.width() / 2 - width
        self.y = scene.height() / 2 - height
        self.width = width
        self.height = height
        self.component_name = component_name
        self.name = name
        self.to_export = 1
        self.scene = scene

        # initializing to (0, 0) so that future positions are relative to (0, 0)
        self.rect = QGraphicsRectItem(0, 0, width, height)
        self.rect.setBrush(QColor("White"))

        # textbox to display component name
        self.text = QGraphicsTextItem(component_name)
        self.text.setPos(self.rect.boundingRect().center() - self.text.boundingRect().center())

        # textbox to display symObject name
        self.name_text = QGraphicsTextItem(name)

        # create delete button
        self.deleteButton = QGraphicsTextItem('X')
        self.deleteButton.setPos(self.rect.boundingRect().topRight() -
                                    self.deleteButton.boundingRect().topRight())
        self.deleteButton.hide()

        # create ports
        port1 = QGraphicsEllipseItem(width/2 - config.port_size/2, height,
                                        config.port_size, config.port_size)
        port1.setBrush(QColor("Black"))

        port2 = QGraphicsEllipseItem(width/2 - config.port_size/2,
                        -config.port_size, config.port_size, config.port_size)
        port2.setBrush(QColor("Black"))

        # add objects created above to group
        self.addToGroup(self.rect)
        self.addToGroup(self.name_text)
        self.addToGroup(self.text)
        self.addToGroup(port1)
        self.addToGroup(port2)
        self.addToGroup(self.deleteButton)

        # set flags
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

        # if we are loading from a file, we dont need to check for overlapping
        # and can set position
        if loadingFromFile:
            self.x = x
            self.y = y
            self.setPos(x, y)
            config.coord_map[(self.x, self.y)] = self.name
            return

        # set initial position to center of scene
        self.setPos(scene.width()/2 - width, scene.height()/2 - height)

        # iterate through existing objects and check if current object overlaps
        # with any of them
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
        # might need this code for attaching objects later
        # if config.sym_objects:
        #     print("skjfdns")
        #     for object in config.sym_objects.values():
        #         object.addToGroup(self)
        #         break
        config.current_sym_object = self

    #register mouse press events
    def mousePressEvent(self, event):
        super(SymObject, self).mousePressEvent(event)

        # hide button on previously selected object
        if config.current_sym_object:
            config.current_sym_object.deleteButton.hide()
        # show button for current object
        self.deleteButton.show()

        # check if mouse press is on delete button
        deletePressed = self.deleteButtonPressed()
        if deletePressed:
            print("Deleting", self.name)
            self.delete()
            return

        # set currentsymobject to self and update attributes for it
        config.current_sym_object = self
        config.mainWindow.populateAttributes(None, self.component_name, False)

    # remove visual and backend respresentations of object
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
                    #self.setPos(self.x, self.y)
                    item.removeFromGroup(item.rect)
                    config.scene.removeItem(item.rect)
                    item.removeFromGroup(item.name_text)
                    item.removeFromGroup(item.text)
                    item.removeFromGroup(item.deleteButton)
                    item.rect = QGraphicsRectItem(item.x, item.y, 300, 300)
                    item.rect.setBrush(QColor("White"))
                    item.addToGroup(item.rect)
                    item.addToGroup(item.name_text)
                    item.addToGroup(item.deleteButton)
                    item.addToGroup(item.text)
                    item.addToGroup(self)
                    return

        # update the object's position parameters
        del config.coord_map[(self.x, self.y)]
        self.x = self.pos().x()
        self.y = self.pos().y()
        config.coord_map[(self.x, self.y)] = self.name

    # checks if the delete button was pressed
    def deleteButtonPressed(self):
        click_x, click_y = self.getClickCoords(self.deleteButton)
        click_x = click_x - self.x
        click_y = click_y - self.y

        deleteButton_x = self.deleteButton.pos().x()
        deleteButton_y = self.deleteButton.pos().y()

        if (abs(click_x - deleteButton_x) <= 5) and \
            (abs(click_y - deleteButton_y) <= 5):
            return True

        return False

    # get coordinates of current mouse clock
    def getClickCoords(self, item):
        cursor_position = QCursor.pos() #global cursor position
        current_view = config.scene.views()[0]
        scene_position = current_view.mapFromGlobal(cursor_position)

        width = item.boundingRect().width()
        height = item.boundingRect().height()

        drop_x = scene_position.x()
        drop_y = scene_position.y()

        return drop_x, drop_y

    # checks if two objects overlap
    def doOverlap(self, l1_x, l1_y, r1_x, r1_y, l2_x, l2_y, r2_x, r2_y):
        notoverlap = l1_x > r2_x or l2_x > r1_x or l1_y > r2_y or l2_y > r1_y
        return not notoverlap
