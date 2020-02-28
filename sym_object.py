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
        self.connected_objects = []
        self.parameters = {}
        self.connections = {}

        # set initial attributes for new symobject
        self.x = scene.width() / 2 - width
        self.y = scene.height() / 2 - height
        self.z = 0
        self.width = width
        self.height = height
        self.component_name = component_name
        self.name = name
        self.parent_name = None
        self.to_export = 1
        self.scene = scene

        self.initUIObject(self, 0, 0)

        # if we are loading from a file, we dont need to check for overlapping
        # and can set position
        if loadingFromFile:
            self.x = x
            self.y = y
            self.setPos(x, y)
            config.coord_map[(self.x, self.y)] = self.name
            return

        # set initial position to center of scene
        self.setPos(scene.width() / 2 - width, scene.height() / 2 - height)

        # iterate through existing objects and check if current object overlaps
        # with any of them
        for key in config.sym_objects:
            item = config.sym_objects[key]
            if self.doesOverlap(item):
                self.setPos(item.x + item.width + 10, item.y + item.height + 10)
                #del config.coord_map[(self.x, self.y)]
                self.x = self.pos().x()
                self.y = self.pos().y()
                config.coord_map[(self.x, self.y)] = self.name

        self.x = self.pos().x()
        self.y = self.pos().y()
        config.coord_map[(self.x, self.y)] = self.name
        config.current_sym_object = self



    def initUIObject(self, object, x, y):
        # initializing to (x, y) so that future positions are relative to (x, y)
        object.rect = QGraphicsRectItem(x, y, object.width, object.height)
        object.rect.setBrush(QColor("White"))

        # textbox to display component name
        object.text = QGraphicsTextItem(object.component_name)
        object.text.setPos(object.rect.boundingRect().center()
                            - object.text.boundingRect().center())

        # textbox to display symObject name
        object.name_text = QGraphicsTextItem(object.name)
        object.name_text.setPos(object.rect.boundingRect().topLeft())

        # create delete button
        object.deleteButton = QGraphicsTextItem('X')
        object.deleteButton.setPos(object.rect.boundingRect().topRight() -
                                object.deleteButton.boundingRect().topRight())
        object.deleteButton.hide()

        # add objects created above to group
        object.addToGroup(object.rect)
        object.addToGroup(object.name_text)
        object.addToGroup(object.text)
        object.addToGroup(object.deleteButton)

        # set flags
        object.setAcceptDrops(True)
        object.setFlag(QGraphicsItem.ItemIsMovable, True)

    #register mouse press events
    def mousePressEvent(self, event):
        self.attachChildren()
        super(SymObject, self).mousePressEvent(event)

        # hide button on previously selected object
        if config.current_sym_object:
            config.current_sym_object.deleteButton.hide()

        # show button for current object
        self.deleteButton.show()

        # check if mouse press is on delete button
        deletePressed = self.deleteButtonPressed(event)
        if deletePressed:
            self.delete()
            return

        # set currentsymobject to self and update attributes for it
        config.current_sym_object = self
        config.mainWindow.populateAttributes(None, self.component_name, False)

    # remove visual and backend respresentations of object
    # delete children as well?
    def delete(self):
        name = self.name
        config.scene.removeItem(self)
        if self.parent_name:
            config.sym_objects[self.parent_name].connected_objects.remove(name)
        for child_name in self.connected_objects:
            #config.sym_objects[child_name].delete()
            del config.coord_map[(config.sym_objects[child_name].x, config.sym_objects[child_name].y)]
            del config.sym_objects[child_name]

        config.current_sym_object = None
        del config.coord_map[(self.x, self.y)]
        del config.sym_objects[name]

    # when mouse is release on object, update its position including the case
    # where it overlaps
    def mouseReleaseEvent(self, event):
        super(SymObject, self).mouseReleaseEvent(event)

        if self.x == self.pos().x() and self.y == self.pos().y():
            return

        z_score = -1
        parent = None

        #iterate through all sym objects on the screen and check if the object's
        # current position overlaps with any of them
        parent = self.getFrontmostOverLappingObject()

        if parent:
            print(parent.name)
            self.resizeUIObject(parent, 0)
            self.parent_name = parent.name # add new parent
            self.z = parent.z + 1 # update z index
            if not self.name in parent.connected_objects:
                parent.connected_objects.append(self.name) # add new child

        # update the object's position parameters
        #del config.coord_map[(self.x, self.y)]
        self.x = self.pos().x()
        self.y = self.pos().y()
        config.coord_map[(self.x, self.y)] = self.name
        self.detachChildren()

    def getFrontmostOverLappingObject(self):
        frontmost_object = None
        highest_zscore = -1
        for key in config.sym_objects:
            object = config.sym_objects[key]
            if self != object and not self.isAncestor(object) and \
               not self.isDescendant(object):
                if self.doesOverlap(object):
                    if object.z > highest_zscore:
                        highest_zscore = object.z
                        frontmost_object = object

        return frontmost_object


    def isAncestor(self, item):
        if not self.parent_name:
            return False
        current_item = self
        while current_item.parent_name:
            if current_item.parent_name == item.name:
                return True
            current_item = config.sym_objects[current_item.parent_name]
        return False


    def isDescendant(self, item):
        if item.name in self.connected_objects:
            return True
        for child_name in self.connected_objects:
            return config.sym_objects[child_name].isDescendant(item)
        return False

    # checks if the delete button was pressed based on mouse click
    def deleteButtonPressed(self, event):
        # get x and y coordinate of mouse click
        click_x, click_y = event.pos().x(), event.pos().y()

        # get coordinate and dimension info from deletebutton
        delete_button_x = self.deleteButton.pos().x()
        delete_button_y = self.deleteButton.pos().y()
        delete_button_width = self.deleteButton.boundingRect().size().width()
        delete_button_height = self.deleteButton.boundingRect().size().height()

        # if the click position is within the text item's bounding box, return
        # true
        if (click_x > delete_button_x and click_x < delete_button_x + \
            delete_button_width and click_y > delete_button_y and click_y < \
            delete_button_y + delete_button_width):
            return True

        return False

    # checks if two objects overlap
    def doesOverlap(self, item):
        l1_x = self.pos().x()
        l1_y = self.pos().y()
        r1_x = self.pos().x() + self.width
        r1_y = self.pos().y() + self.height
        l2_x = item.x
        l2_y = item.y
        r2_x = item.x + item.width
        r2_y = item.y + item.height
        notoverlap = l1_x > r2_x or l2_x > r1_x or l1_y > r2_y or l2_y > r1_y
        return not notoverlap

    # resizes a sym_object when another object is placed in it
    def resizeUIObject(self, item, force_resize):
        item.removeFromGroup(item.rect)
        config.scene.removeItem(item.rect)
        item.removeFromGroup(item.name_text)
        config.scene.removeItem(item.name_text)
        item.removeFromGroup(item.text)
        config.scene.removeItem(item.text)
        item.removeFromGroup(item.deleteButton)
        config.scene.removeItem(item.deleteButton)
        item.x = item.pos().x()
        item.y = item.pos().y()

        if not item.connected_objects: # or force_resize:
            item.width += 120
            item.height += 120
            self.setPos(item.x, item.y + item.height - self.height)

        rightmost_object = item.rightMostChild(self)
        lowest_object = item.lowestChild(self)

        y_diff = lowest_object.pos().y() + lowest_object.height - item.pos().y() - item.height
        x_diff = item.pos().x() + item.width - rightmost_object.pos().x() - rightmost_object.width

        if item.connected_objects:
            if x_diff < 120:
                item.width += 120
            if y_diff > 0:
                item.height += y_diff

            next_x = item.x

            for child in item.connected_objects:
                cur_child = config.sym_objects[child]
                child_y = item.y + item.height - cur_child.height
                cur_child.setPos(next_x, child_y)
                if cur_child.connected_objects:
                    next_x += (120 * len(cur_child.connected_objects)) + 10 + 120
                else:
                    next_x += cur_child.width + 10

            if not force_resize:
                self.setPos(next_x, child_y)

        if item.parent_name:
            item.resizeUIObject(config.sym_objects[item.parent_name], 1)
            # if not item.connected_objects:
            #     item.resizeUIObject(config.sym_objects[item.parent_name], 1)
            # else:
            #     item.resizeUIObject(config.sym_objects[item.parent_name], 0)

        self.initUIObject(item, item.x, item.y)

    def lowestChild(parent, item):
        lowest = item
        y_coord = item.pos().x() + item.width
        for child in parent.connected_objects:
            cur_child = config.sym_objects[child]
            if (cur_child.pos().y() + cur_child.height > y_coord):
                y_coord = cur_child.pos().y() + cur_child.height
                lowest = cur_child

        return lowest

    def rightMostChild(parent, item):
        rightmost = item
        x_coord = item.pos().x() + item.width
        for child in parent.connected_objects:
            cur_child = config.sym_objects[child]
            if (cur_child.pos().x() + cur_child.width > x_coord):
                x_coord = cur_child.pos().x() + cur_child.width
                rightmost = cur_child

        return rightmost

    # attaches all children of the current sym_object to it so they move as one
    def attachChildren(self):
        for child_name in self.connected_objects:
            self.addToGroup(config.sym_objects[child_name])
            config.sym_objects[child_name].attachChildren() #attach descendants

    # detaches children to allow for independent movement
    def detachChildren(self):
        for child_name in self.connected_objects:
            #config.sym_objects[child_name].detachChildren()
            self.removeFromGroup(config.sym_objects[child_name])
