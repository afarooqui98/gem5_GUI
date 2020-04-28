from lineDrawer import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from gui_views import state
from m5_calls import *
import copy

class SymObject(QGraphicsItemGroup):

    def __init__(self, x, y, width, height, scene, component_name, name,
                    loadingFromFile, state, display_name):
        super(SymObject, self).__init__()

        #common variables
        self.state = state
        self.component_name = component_name
        self.connected_objects = []
        self.parent_name = None
        self.scene = scene

        #backend members
        #instance_ports and instance_params: keep metadata about connections
        #and are employed to make connections via m5

        #sim_object and sim_object_instance: former is class, latter is class
        #instance
        self.instance_params = {}
        self.instance_ports = {}
        self.sim_object = \
            copy.deepcopy(
            self.state.instances[self.component_name])
        self.sim_object_instance = None

        #ui members
        #    rect, rect_text, ui_ports, delete_button: define the QGraphicsItem
        #    that shows up in the gui

        #    ui_connections: lineDrawer instances that allow user to draw lines
        self.x = scene.width() / 2 - width
        self.y = scene.height() / 2 - height
        self.z = 0
        self.width = width
        self.height = height
        self.name = name
        self.display_name = display_name
        self.rect = None
        self.rect_text = None
        self.delete_button = None
        self.delete
        self.ui_ports = []
        self.ui_connections = {}

        #constructing the baseline ui elements
        self.initUIObject(self, 0, 0)
        # if we are loading from a file, we dont need to check for overlapping
        # and can set position. If x == -1, we are importing an object
        if loadingFromFile and x != -1:
            self.x = x
            self.y = y
            self.setPos(x, y)
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

        self.x = self.scenePos().x()
        self.y = self.scenePos().y()
        self.state.removeHighlight()
        del self.state.selected_sym_objects[:]
        self.state.selected_sym_objects.append(self)

    def get_param_info(self):
        """Get additional info on params such as default values  after
        instantiating object. This information is held in a dictionary produced
        from calling enumerate_params method on instantiated object """

        #calling enumerate_params to get exact values for parameters
        param_dict = self.sim_object_instance.enumerateParams()

        for param, value in self.instance_params.items():
            if(isinstance(self.instance_params[param]["Default"], AttrProxy)):
                continue #want to skip proxy parameters, want to do this lazily

            if param_dict.get(param) == None:
                # Some parameters are included in the class but not in the actual
                # parameters given in enumerateParams TODO: look into this
                continue
            else:
                #if we load from a ui file, check if the default and value params
                # are diferent
                if self.instance_params[param]["Value"] != \
                        self.instance_params[param]["Default"]:
                    continue

                if param_dict[param].default_val != "": #if there is a default value
                    default = param_dict[param].default_val
                    self.instance_params[param]["Default"] = default
                    self.instance_params[param]["Value"] = default
                else:
                    continue

    def load_instantiate(self):
        """Instantiation and some paramter/port info collection occurs here when
        an object is loaded from a model file """

        if self.component_name == "Root":
            self.sim_object_instance = getRoot()
        else:
            self.sim_object_instance = self.sim_object()
        param_dict = self.sim_object_instance._params
        port_dict = self.sim_object_instance._ports

        # Some parameters are included in the class but not in the actual instance_params
        #   given in enumerateParams TODO: look into this!!!
        weird_params = []

        for port, port_info in self.instance_ports.items():
            if port_info["Value"] == None:
                port_info["Value"] = port_dict.get(port) #load default port

        for param, param_info in self.instance_params.items():
            if param_dict.get(param) == None:
                weird_params.append(param)
                continue

            #Check is set since some of the types for parametrs are VectorParam objs
            if inspect.isclass(param_dict[param].ptype):
                self.instance_params[param]["Type"] = param_dict[param].ptype
            else:
                self.instance_params[param]["Type"] = type(param_dict[param].ptype)

            self.instance_params[param]["Description"] = param_dict[param].desc

            if hasattr(param_dict[param], 'default'):
                self.instance_params[param]["Default"] = param_dict[param].default
            else:
                self.instance_params[param]["Default"] = None

            #If the value was changed in the model file then no need to load in
            #   the default, otherwise the value is set to the default
            if "Value" not in self.instance_params[param]:
                self.instance_params[param]["Value"] = \
                    self.instance_params[param]["Default"]

        for i in range(len(weird_params)):
            del self.instance_params[weird_params[i]]

        self.get_param_info() #enumerate over params to assign default values

    def instantiateSimObject(self):
        """ Creates an instantiated object for the symobject and gets any new
        info on the instance_params """
        if self.component_name == "Root":
            self.sim_object_instance = getRoot()
        else:
            self.sim_object_instance = self.sim_object()
        self.get_param_info()

    def initPorts(self):
        """Create the display for the ports on the symobjects"""

        del self.ui_ports[:]
        x = self.scenePos().x() + self.width * 3 / 4
        num_ports = len(self.instance_ports)
        delete_button_height = self.delete_button.boundingRect().height()
        next_y = delete_button_height
        for sim_object_instance_port in sorted(self.instance_ports):
            #port = QGraphicsItemGroup()
            # size of port is 25 x 10
            # y + 25 is the y we want to add the port at
            y = self.scenePos().y() + next_y
            port_box = QGraphicsRectItem(x, y, self.width / 4, (self.height - \
                delete_button_height) / num_ports)
            self.addToGroup(port_box)
            port_name = QGraphicsTextItem(sim_object_instance_port)
            font = QFont()
            font.setPointSize(5)
            port_name.setFont(font)
            port_name.setPos(port_box.boundingRect().center() - \
                port_name.boundingRect().center())
            self.addToGroup(port_name)
            self.ui_ports.append((sim_object_instance_port, port_box, port_name))
            next_y += (self.height - delete_button_height) / num_ports

            #self.addToGroup(port)

    def initUIObject(self, object, x, y):
        """creates the QGraphicsItem that shows up in the scene"""

        # initializing to (x, y) so that future positions are relative to (x, y)
        object.rect = QGraphicsRectItem(x, y, object.width, object.height)
        object.rect.setBrush(QColor("White"))

        # textbox to display symObject name
        object.rect_text = QGraphicsTextItem(object.display_name + "::" +
                                                        object.component_name)
        object.rect_text.setPos(object.rect.boundingRect().topLeft())

        # create delete button
        object.delete_button = QGraphicsTextItem('X')
        object.delete_button.setPos(object.rect.boundingRect().topRight() -
                                object.delete_button.boundingRect().topRight())
        object.delete_button.hide()

        # set max width of name, 20 is the width of the delete button
        object.rect_text.setTextWidth(object.width - 20)

        # add objects created above to group
        object.addToGroup(object.rect)
        object.addToGroup(object.rect_text)
        # object.addToGroup(object.text)
        object.addToGroup(object.delete_button)

        # set flags
        object.setAcceptDrops(True)
        object.setFlag(QGraphicsItem.ItemIsMovable, True)

    def mousePressEvent(self, event):
        '''handle required operations when a sym object is clicked on'''
        if not self.state.draw_wire_state:
            self.setCursor(QCursor(Qt.ClosedHandCursor))
        self.state.object_clicked = 1
        modifiers = QApplication.keyboardModifiers()
        if modifiers != Qt.ShiftModifier:
            # hide button on previously selected object
            self.state.removeHighlight()
            del self.state.selected_sym_objects[:]
        # get object that was clicked on (since multiple objects can be stacked
        # on top of each other)
        clicked = self.getClickedObject(event)
        #bring clicked object to foreground so drag events have object clarity
        clicked.setZValue(100)

        if not clicked:
            clicked = self

        clicked.attachChildren()
        super(SymObject, clicked).mousePressEvent(event)

        # show button for current object
        clicked.rect.setBrush(QColor("Green"))

        # check if mouse press is on delete button
        deletePressed = clicked.deleteButtonPressed(event)
        if deletePressed:
            clicked.delete()
            return

        # add clicked to list if not present and update attributes for it
        if not clicked in self.state.selected_sym_objects:
            self.state.selected_sym_objects.append(clicked)
        if len(self.state.selected_sym_objects) == 1:
            clicked.delete_button.show()
            self.state.mainWindow.populateAttributes(None,
                clicked.component_name, False)
        else: #hide attribute table
            table = self.state.mainWindow.attributeView.attributeTable
            table.clear()
            table.setRowCount(0)

    def delete(self):
        """remove visual respresentations of object"""
        #TODO: implement backend removal, possibly in other function
        name = self.name
        self.state.scene.removeItem(self)
        if self.parent_name:
            parent = self.state.sym_objects[self.parent_name]
            parent.connected_objects.remove(name)
            if not parent.connected_objects:
                self.resizeUIObject(parent, 1, 120 - parent.width)

        for child_name in self.connected_objects:
            # delete any connections from/to child
            for key in self.state.sym_objects[child_name].ui_connections.keys():
                if key[0] == "parent":
                    connection = self.state.sym_objects[child_name].\
                                                            ui_connections[key]
                    del self.state.sym_objects[child_name].ui_connections[key]
                else:
                    parent_key = ("parent", str(child_name), key[3], key[2])
                    connection = self.state.sym_objects[key[1]].\
                                                    ui_connections[parent_key]
                    del self.state.sym_objects[key[1]].ui_connections[parent_key]

                if connection.line:
                    self.state.scene.removeItem(connection.line)

            self.state.sym_objects[child_name].ui_connections.clear()

            # remove child
            del self.state.sym_objects[child_name]

        # delete any connections from the object being deleted
        for key in self.ui_connections:
            connection = self.ui_connections[key]
            if connection.line:
                self.state.scene.removeItem(connection.line)

        self.ui_connections.clear()

        del self.state.selected_sym_objects[:]
        del self.state.sym_objects[name]
        self.state.mostRecentSaved = False


    def mouseMoveEvent(self, event):
        '''handle changes when symobject is moved around on canvas'''
        if self.state.object_clicked:
            self.modifyConnections(event, self)
            self.updateChildrenConnections(event, self)
            self.state.line_drawer.update()
            super(SymObject, self).mouseMoveEvent(event)
            self.state.mostRecentSaved = False
        else:
            if not self.state.draw_wire_state:
                self.setCursor(QCursor(Qt.PointingHandCursor))

    def modifyConnections(self, event, sym_object):
        '''update connection position information when an object is dragged
        around'''
        # set connection to middle of port
        num_ports = len(sym_object.instance_ports)
        if not num_ports:
            return

        delete_button_height = sym_object.delete_button.boundingRect().height()
        y_offset = (sym_object.height - delete_button_height) / num_ports
        new_x = sym_object.scenePos().x() + sym_object.width * 7 / 8

        for name, connection in sym_object.ui_connections.items():
            new_y = delete_button_height
            if name[0] == "parent":
                new_y += sym_object.scenePos().y() + connection.parent_port_num\
                    * y_offset + y_offset / 4
                new_coords = QPointF(new_x, new_y)
                key = ("child", sym_object.name, name[3], name[2])
                connection.setEndpoints(new_coords, None)
                self.state.sym_objects[name[1]].ui_connections[key].setEndpoints(\
                                                            new_coords, None)
            else:
                new_y += sym_object.scenePos().y() + connection.child_port_num \
                    * y_offset + y_offset / 4
                new_coords = QPointF(new_x, new_y)
                key = ("parent", sym_object.name, name[3], name[2])
                connection.setEndpoints(None, new_coords)
                self.state.sym_objects[name[1]].ui_connections[key].setEndpoints(\
                                                            None, new_coords)


    def updateChildrenConnections(self, event, sym_object):
        """update all child connections"""
        for object_name in sym_object.connected_objects:
            object = self.state.sym_objects[object_name]
            self.modifyConnections(event, object)
            self.updateChildrenConnections(event, object)

    def mouseReleaseEvent(self, event):
        """when mouse is release on object, update its position including the case
        where it overlaps and deal with subobject being created"""
        self.state.object_clicked = 0
        if not self.state.draw_wire_state:
            self.setCursor(QCursor(Qt.PointingHandCursor))
        super(SymObject, self).mouseReleaseEvent(event)

        # if object has not moved
        if self.x == self.pos().x() and self.y == self.pos().y():
            return

        #iterate through all sym objects on the screen and check if the object's
        # current position overlaps with any of them
        parent = self.getFrontmostOverLappingObject()

        # if an overlapping object is found -> resize, update parent name AND
        # add self to the parent's list of children
        if parent:
            self.resizeUIObject(parent, 1, self.width)
            self.parent_name = parent.name # add new parent
            self.z = parent.z + 1 # update z index

            # update child z indices
            for child in self.connected_objects:
                self.state.sym_objects[child].z = self.z + 1

            if not self.name in parent.connected_objects:
                parent.connected_objects.append(self.name) # add new child
        else:
            if self.parent_name and not self.doesOverlap(self.state.sym_objects[self.parent_name]):
                # if the object is dragged out of a parent, remove the parent,
                # child relationship
                curParent = self.state.sym_objects[self.parent_name]
                curParent.resizeParent(self)
                curParent.connected_objects.remove(self.name)
                self.parent_name = None


        for object in self.state.sym_objects.values():
            object.setZValue(object.z)

        # update the object's position instance_params
        self.x = self.scenePos().x()
        self.y = self.scenePos().y()
        self.detachChildren()
        self.state.line_drawer.update()
        self.state.mostRecentSaved = False


    def hoverEnterEvent(self, event):
        if not self.state.draw_wire_state:
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def hoverLeaveEvent(self, event):
        if not self.state.draw_wire_state:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def getClickedObject(self, event):
        """based on mouse click position, return object with highest zscore"""
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

    def getFrontmostOverLappingObject(self):
        """based on object being dragged, return object with highest zscore"""
        frontmost_object = None
        highest_zscore = -1
        for key in self.state.sym_objects:
            object = self.state.sym_objects[key]
            #if two objects are related
            if self != object and not self.isAncestor(object) and \
                not self.isDescendant(object):
                if self.doesOverlap(object):
                    if object.z > highest_zscore:
                        highest_zscore = object.z
                        frontmost_object = object

        return frontmost_object

    def isClicked(self, event):
        """determine if a symobject was clicked on given the position of the
        click"""
        click_x, click_y = event.scenePos().x(), event.scenePos().y()
        # return if the click position is within the text item's bounding box
        if (click_x > self.scenePos().x() and click_x < self.scenePos().x() + \
            self.width and click_y > self.scenePos().y() and click_y < \
            self.scenePos().y() + self.height):
            return True

        return False

    def isAncestor(self, item):
        """determine if item is an ancestor of self"""
        if not self.parent_name:
            return False
        current_item = self
        while current_item.parent_name:
            if current_item.parent_name == item.name:
                return True
            current_item = self.state.sym_objects[current_item.parent_name]
        return False

    def isDescendant(self, item):
        """determine if item is a descendant of self"""
        if item.name in self.connected_objects:
            return True
        for child_name in self.connected_objects:
            return self.state.sym_objects[child_name].isDescendant(item)
        return False

    def deleteButtonPressed(self, event):
        """checks if the delete button was pressed based on mouse click"""

        # get x and y coordinate of mouse click
        click_x, click_y = event.scenePos().x(), event.scenePos().y()

        # get coordinate and dimension info from delete_button
        delete_button_x = self.delete_button.scenePos().x()
        delete_button_y = self.delete_button.scenePos().y()
        delete_button_width = self.delete_button.boundingRect().size().width()
        delete_button_height = self.delete_button.boundingRect().size().height()

        # if the click position is within the text item's bounding box, return
        # true
        if (click_x > delete_button_x and click_x < delete_button_x + \
            delete_button_width and click_y > delete_button_y and click_y < \
            delete_button_y + delete_button_width):
            return True

        return False

    def doesOverlap(self, item):
        """checks if two objects overlap"""

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

    def resizeUIObject(self, item, force_resize, size):
        """resizes a sym_object when another object is placed in it"""
        item.removeUIObjects()

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
        """finds a parent's lowest child"""
        lowest = item
        y_coord = item.scenePos().y() + item.height
        for child in self.connected_objects:
            cur_child = self.state.sym_objects[child]
            if (cur_child.scenePos().y() + cur_child.height > y_coord):
                y_coord = cur_child.scenePos().y() + cur_child.height
                lowest = cur_child

        return lowest

    def rightMostChild(self, item):
        """finds a parent's rightmost child"""
        rightmost = item
        x_coord = item.scenePos().x() + item.width
        for child in self.connected_objects:
            cur_child = self.state.sym_objects[child]
            if (cur_child.scenePos().x() + cur_child.width > x_coord):
                x_coord = cur_child.scenePos().x() + cur_child.width
                rightmost = cur_child

        return rightmost

    def attachChildren(self):
        """attaches all children of the current sym_object to
        it so they move as one"""

        for child_name in self.connected_objects:
            self.addToGroup(self.state.sym_objects[child_name])
            #attach descendants
            self.state.sym_objects[child_name].attachChildren()

    def detachChildren(self):
        """detaches children to allow for independent movement"""

        for child_name in self.connected_objects:
            self.removeFromGroup(self.state.sym_objects[child_name])

    def updateName(self, newName):
        """updates a symobjects name"""

        # changed name on visualization of symobject
        self.rect_text.setPlainText(newName + "::" + self.component_name)

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

        # update the current object's name in each of its connections'
        # connection list
        for ui_connection in self.ui_connections:
            connected_object_name = ui_connection[1]
            connected_object = self.state.sym_objects[connected_object_name]
            for connection in connected_object.ui_connections:
                if connection[1] == self.name:
                    value = connected_object.ui_connections[connection]
                    del connected_object.ui_connections[connection]
                    new_key = (connection[0], newName, connection[2],
                                connection[3])
                    connected_object.ui_connections[new_key] = value

        # update member variable
        self.display_name = newName


    def addSubObject(self, child):
        '''add child to parent's (self's) UI object and setting parameters'''
        child.resizeUIObject(self, 1, child.width)
        child.parent_name = self.name
        child.z = self.z + 1
        if not child.name in self.connected_objects:
            self.connected_objects.append(child.name)

        for object in self.state.sym_objects.values():
            object.setZValue(object.z)

    def resizeParent(self, child):
        '''reduce the size of the parent if it has one child'''
        self.removeUIObjects()

        if len(self.connected_objects) == 1:
            self.width -= child.width
            self.height -= child.width

        self.initUIObject(self, self.x, self.y)
        self.initPorts()

    def removeUIObjects(self):
        '''disconnect all the symobjects components before it is resized'''
        self.removeFromGroup(self.rect)
        self.state.scene.removeItem(self.rect)
        self.removeFromGroup(self.rect_text)
        self.state.scene.removeItem(self.rect_text)
        self.removeFromGroup(self.delete_button)
        self.state.scene.removeItem(self.delete_button)
        for port in self.ui_ports:
            port_box = port[1]
            port_name = port[2]
            self.removeFromGroup(port_box)
            self.state.scene.removeItem(port_box)
            self.removeFromGroup(port_name)
            self.state.scene.removeItem(port_name)

    def getDisplayNames(self, sym_object_ids):
        """convert list of backend sym object ids to their display names"""
        names = []
        for id in sym_object_ids:
            names.append(self.state.sym_objects[id].display_name)

        return names
