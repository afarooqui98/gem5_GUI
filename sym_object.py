from lineDrawer import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from gui_views import state
from m5_calls import *


class SymObject(QGraphicsItemGroup):

    def __init__(self, x, y, width, height, scene, component_name, name,
                    loadingFromFile, state):
        super(SymObject, self).__init__()
        self.state = state
        self.connected_objects = []
        self.parameters = {}
        self.ports = {}
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
            self.state.coord_map[(self.x, self.y)] = self.name
            return

        # set initial position to center of scene
        self.setPos(scene.width() / 2 - width, scene.height() / 2 - height)

        # iterate through existing objects and check if current object overlaps
        # with any of them
        for key in self.state.sym_objects:
            item = self.state.sym_objects[key]
            if self.doesOverlap(item):
                self.setPos(item.scenePos().x() + item.width + 10,
                            item.scenePos().y() + item.height + 10)
                self.x = self.scenePos().x()
                self.y = self.scenePos().y()
                self.state.coord_map[(self.x, self.y)] = self.name

        self.x = self.scenePos().x()
        self.y = self.scenePos().y()
        self.state.coord_map[(self.x, self.y)] = self.name
        self.state.current_sym_object = self

    def instantiateSimObject(self):
        object_instantiate(self) #actual simobject

    def initPorts(self):
        self.sym_ports = []
        x = self.scenePos().x() + self.width * 3 / 4
        num_ports = len(self.ports)
        delete_button_height = self.deleteButton.boundingRect().height()
        next_y = delete_button_height
        for sim_object_port in self.ports:
            #port = QGraphicsItemGroup()
            # size of port is 25 x 10
            # y + 25 is the y we want to add the port at
            y = self.scenePos().y() + next_y
            port_box = QGraphicsRectItem(x, y, self.width / 4, (self.height - \
                delete_button_height) / num_ports)
            self.addToGroup(port_box)
            port_name = QGraphicsTextItem(sim_object_port)
            font = QFont()
            font.setPointSize(5)
            port_name.setFont(font)
            port_name.setPos(port_box.boundingRect().center() - \
                port_name.boundingRect().center())
            self.addToGroup(port_name)
            self.sym_ports.append((sim_object_port, port_box))
            next_y += (self.height - delete_button_height) / num_ports

            #self.addToGroup(port)

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
        # get object that was clicked on (since multiple objects can be stacked
        # on top of each other)
        clicked = self.getClickedObject(event)
        clicked.setZValue(100)
        if not clicked:
            clicked = self

        clicked.attachChildren()
        super(SymObject, clicked).mousePressEvent(event)

        # hide button on previously selected object
        if self.state.current_sym_object:
            self.state.current_sym_object.deleteButton.hide()

        # show button for current object
        clicked.deleteButton.show()

        # check if mouse press is on delete button
        deletePressed = clicked.deleteButtonPressed(event)
        if deletePressed:
            clicked.delete()
            return

        # set currentsymobject to self and update attributes for it
        self.state.current_sym_object = clicked
        self.state.mainWindow.populateAttributes(None,
            clicked.component_name, False)
        self.state.line_drawer.draw_lines = 1

    # remove visual and backend respresentations of object
    def delete(self):
        name = self.name
        self.state.scene.removeItem(self)
        if self.parent_name:
            parent = self.state.sym_objects[self.parent_name]
            parent.connected_objects.remove(name)
            if not parent.connected_objects:
                self.resizeUIObject(parent, 1, 120 - parent.width)
        for child_name in self.connected_objects:
            #self.state.sym_objects[child_name].delete()
            del self.state.coord_map[(self.state.sym_objects[child_name].x, \
                self.state.sym_objects[child_name].y)]
            del self.state.sym_objects[child_name]

        self.state.current_sym_object = None
        del self.state.coord_map[(self.x, self.y)]
        del self.state.sym_objects[name]


    def mouseMoveEvent(self, event):
        self.modifyConnections(event, self)
        self.updateChildrenConnections(event, self)
        self.state.line_drawer.update()
        super(SymObject, self).mouseMoveEvent(event)

    def modifyConnections(self, event, sym_object):
        #middle of port
        num_ports = len(sym_object.ports)
        if not num_ports:
            return

        delete_button_height = sym_object.deleteButton.boundingRect().height()
        y_offset = (sym_object.height - delete_button_height) / num_ports
        new_x = sym_object.scenePos().x() + sym_object.width * 7 / 8

        for name, connection in sym_object.connections.items():
            new_y = delete_button_height
            if name[0] == "parent":
                new_y += sym_object.scenePos().y() + connection.parent_port_num\
                    * y_offset + y_offset / 4
                new_coords = QPointF(new_x, new_y)
                key = ("child", sym_object.name, name[3], name[2])
                connection.setEndpoints(new_coords, None)
                self.state.sym_objects[name[1]].connections[key].setEndpoints(\
                                                            new_coords, None)
            else:
                new_y += sym_object.scenePos().y() + connection.child_port_num \
                    * y_offset + y_offset / 4
                new_coords = QPointF(new_x, new_y)
                key = ("parent", sym_object.name, name[3], name[2])
                connection.setEndpoints(None, new_coords)
                self.state.sym_objects[name[1]].connections[key].setEndpoints(\
                                                            None, new_coords)


    def updateChildrenConnections(self, event, sym_object):
        for object_name in sym_object.connected_objects:
            object = self.state.sym_objects[object_name]
            self.modifyConnections(event, object)
            self.updateChildrenConnections(event, object)

    # when mouse is release on object, update its position including the case
    # where it overlaps and deal with subobject being created
    def mouseReleaseEvent(self, event):
        super(SymObject, self).mouseReleaseEvent(event)

        # if object has not moved
        if self.x == self.pos().x() and self.y == self.pos().y():
            return

        z_score = -1
        parent = None
        #iterate through all sym objects on the screen and check if the object's
        # current position overlaps with any of them
        parent = self.getFrontmostOverLappingObject()

        # if an overlapping object is found -> resize, update parent name AND
        # add self to the parent's list of children
        if parent:
            self.resizeUIObject(parent, 1, self.width)
            self.parent_name = parent.name # add new parent
            self.z = parent.z + 1 # update z index
            if not self.name in parent.connected_objects:
                parent.connected_objects.append(self.name) # add new child
        for object in self.state.sym_objects.values():
            object.setZValue(object.z)
        # update the object's position parameters
        #del self.state.coord_map[(self.x, self.y)]
        self.x = self.scenePos().x()
        self.y = self.scenePos().y()
        self.detachChildren()
        self.state.line_drawer.update()

    # based on mouse click position, return object with highest zscore
    def getClickedObject(self, event):
        frontmost_object = None
        highest_zscore = -1
        for key in self.state.sym_objects:
            object = self.state.sym_objects[key]
            if object.isClicked(event):
                if object.z > highest_zscore:
                    highest_zscore = object.z
                    frontmost_object = object

        if (self.z > highest_zscore):
            frontmost_object = self

        return frontmost_object

    # based on object being dragged, return object with highest zscore
    def getFrontmostOverLappingObject(self):
        frontmost_object = None
        highest_zscore = -1
        for key in self.state.sym_objects:
            object = self.state.sym_objects[key]
            if self != object and not self.isAncestor(object) and \
               not self.isDescendant(object):
                if self.doesOverlap(object):
                    if object.z > highest_zscore:
                        highest_zscore = object.z
                        frontmost_object = object

        return frontmost_object

    def isClicked(self, event):
        click_x, click_y = event.scenePos().x(), event.scenePos().y()
        # if the click position is within the text item's bounding box, return
        # true
        if (click_x > self.scenePos().x() and click_x < self.scenePos().x() + \
            self.width and click_y > self.scenePos().y() and click_y < \
            self.scenePos().y() + self.height):
            return True

        return False

    def isAncestor(self, item):
        if not self.parent_name:
            return False
        current_item = self
        while current_item.parent_name:
            if current_item.parent_name == item.name:
                return True
            current_item = self.state.sym_objects[current_item.parent_name]
        return False

    def isDescendant(self, item):
        if item.name in self.connected_objects:
            return True
        for child_name in self.connected_objects:
            return self.isDescendant(self.state.sym_objects[child_name])
        return False

    # checks if the delete button was pressed based on mouse click
    def deleteButtonPressed(self, event):
        # get x and y coordinate of mouse click
        click_x, click_y = event.scenePos().x(), event.scenePos().y()

        # get coordinate and dimension info from deletebutton
        delete_button_x = self.deleteButton.scenePos().x()
        delete_button_y = self.deleteButton.scenePos().y()
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
        l1_x = self.scenePos().x()
        l1_y = self.scenePos().y()
        r1_x = self.scenePos().x() + self.width
        r1_y = self.scenePos().y() + self.height
        l2_x = item.scenePos().x()
        l2_y = item.scenePos().y()
        r2_x = item.scenePos().x() + item.width
        r2_y = item.scenePos().y() + item.height
        notoverlap = l1_x > r2_x or l2_x > r1_x or l1_y > r2_y or l2_y > r1_y
        return not notoverlap

    # resizes a sym_object when another object is placed in it
    def resizeUIObject(self, item, force_resize, size):
        item.removeFromGroup(item.rect)
        self.state.scene.removeItem(item.rect)
        item.removeFromGroup(item.name_text)
        self.state.scene.removeItem(item.name_text)
        item.removeFromGroup(item.text)
        self.state.scene.removeItem(item.text)
        item.removeFromGroup(item.deleteButton)
        self.state.scene.removeItem(item.deleteButton)
        for port in item.sym_ports:
            port_box = port[1]
            item.removeFromGroup(port_box)
            self.state.scene.removeItem(port_box)

        item.x = item.scenePos().x()
        item.y = item.scenePos().y()

        # if item is a new parent
        if not item.connected_objects: # or force_resize:
            item.width += self.width
            item.height += self.width

            self.setPos(item.scenePos().x(),
                        item.scenePos().y() + item.height - self.height)
            self.x = self.scenePos().x()
            self.y = self.scenePos().y()

        # get rightmost and lowest child for dynamic resizing in case a child
        # if not within bounds of parent
        rightmost_object = item.rightMostChild(self)
        lowest_object = item.lowestChild(self)

        y_diff = lowest_object.scenePos().y() + lowest_object.height - \
            item.scenePos().y() - item.height
        x_diff = item.scenePos().x() + item.width - \
                        rightmost_object.scenePos().x() - rightmost_object.width

        if item.connected_objects:
            if x_diff < size:
                item.width += size
            if y_diff > 0:
                item.height += y_diff

            # place first child at x coordinate of parent
            next_x = item.scenePos().x()

            # re-render all children to deal with any cases of nested children
            # being resized
            # print(item.name, item.scenePos().x(), item.scenePos().y())
            # for child in item.connected_objects:
            #     cur_child = self.state.sym_objects[child]
            #     child_y = item.scenePos().y() + item.height - cur_child.height
            #     cur_child.setPos(next_x, child_y)
            #     cur_child.x = cur_child.scenePos().x()
            #     cur_child.y = cur_child.scenePos().y()
            #     next_x += cur_child.width + 10
            #     print(cur_child.name, cur_child.scenePos().x(), cur_child.scenePos().y())


            # if not force_resize:
            #     self.setPos(next_x, child_y)
            #     self.x = self.scenePos().x()
            #     self.y = self.scenePos().y()

        # recursively traverse upwards and resize each parent
        if item.parent_name:
            item.resizeUIObject(self.state.sym_objects[item.parent_name], \
            1, size)

        self.initUIObject(item, item.x, item.y)
        item.initPorts()
        self.modifyConnections(item, item)
        self.updateChildrenConnections(item, item)
        self.state.line_drawer.update()

    def lowestChild(self, item):
        lowest = item
        y_coord = item.scenePos().y() + item.height
        for child in self.connected_objects:
            cur_child = self.state.sym_objects[child]
            if (cur_child.scenePos().y() + cur_child.height > y_coord):
                y_coord = cur_child.scenePos().y() + cur_child.height
                lowest = cur_child

        return lowest

    def rightMostChild(self, item):
        rightmost = item
        x_coord = item.scenePos().x() + item.width
        for child in self.connected_objects:
            cur_child = self.state.sym_objects[child]
            if (cur_child.scenePos().x() + cur_child.width > x_coord):
                x_coord = cur_child.scenePos().x() + cur_child.width
                rightmost = cur_child

        return rightmost

    # attaches all children of the current sym_object to it so they move as one
    def attachChildren(self):
        for child_name in self.connected_objects:
            print(child_name)
            self.addToGroup(self.state.sym_objects[child_name])
            #attach descendants
            self.state.sym_objects[child_name].attachChildren()

    # detaches children to allow for independent movement
    def detachChildren(self):
        for child_name in self.connected_objects:
            #self.state.sym_objects[child_name].detachChildren()
            self.removeFromGroup(self.state.sym_objects[child_name])

    # updates a symobjects name
    def updateName(self, newName):
        # changed name on visualization of symobject
        self.name_text.setPlainText(newName)

        # if sym object has a parent, change current sym object's name in
        # parent's list of child objects
        if self.parent_name:
            self.state.sym_objects[self.parent_name].connected_objects.\
                                                            remove(self.name)
            self.state.sym_objects[self.parent_name].connected_objects.\
                                                            append(newName)

        # if sym object is a parent, change the parent name of all of its
        # children
        if self.connected_objects:
            for child_name in self.connected_objects:
                self.state.sym_objects[child_name].parent_name = newName

        # update member variable
        self.name = newName
