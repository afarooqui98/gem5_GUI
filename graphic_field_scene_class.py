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
from sym_object import *
import string

class FieldGraphicsScene(QGraphicsScene):
    """this class provides a scene to manage items in the field"""

    #constructor
    def __init__(self,max_crops,max_animals):
        super().__init__()
        config.line_drawer = LineDrawer()
        self.field = Field(max_crops,max_animals)
        self.background_brush = QBrush()
        self.addWidget(config.line_drawer)

        config.line_drawer.resize(700, 600)

    def _drop_position(self,item):
        cursor_position = QCursor.pos() #global cursor position
        current_view = self.views()[0]
        scene_position = current_view.mapFromGlobal(cursor_position)

        width = item.boundingRect().width()
        height = item.boundingRect().height()

        width_offset = width / 2
        height_offset = height / 2

        drop_x = scene_position.x() - width_offset
        drop_y = scene_position.y() - height_offset

        return drop_x, drop_y


    def loadSavedObject(self, type, name, newObject):

        x = newObject["x"]
        y = newObject["y"]
        component_name = newObject["component_name"]
        parameters = newObject["parameters"]

        if component_name == "System":
            new_object = SymObject(0, 0, 500, 500, self, component_name, name, True)
        else:
            new_object = SymObject(x, y, 100, 50, self, component_name, name, True)

        new_object.setFlag(QGraphicsItem.ItemIsMovable, True)
        new_object.parameters = parameters

        config.sym_objects[name] = new_object
        config.current_sym_object = new_object
        self.addItem(new_object)
        return new_object

    def _visualise_graphic_item_center(self, type, component_name, name):

        if not name:
            name = ''.join(random.choice(string.ascii_lowercase) for i in range(7))

        if component_name == "System":
            new_object = SymObject(0, 0, 500, 500, self, component_name, name, False)
        else:
            new_object = SymObject(0, 0, 100, 50, self, component_name, name, False)

        new_object.setFlag(QGraphicsItem.ItemIsMovable, True)

        #config.coord_map[(new_object.x, new_object.y)] = name
        config.sym_objects[name] = new_object
        config.current_sym_object = new_object
        self.addItem(new_object)
        return new_object

    def _add_graphic_item(self, result, type, name):
        if result:
            self._visualise_graphic_item_center(type, name)
        else:
            error_message = QMessageBox()
            message = "No more " + graphic_item_type + "s can be added to this field"
            error_message.setText(message)
            error_message.exec()

    #this method overrides the parent method
    def dragEnterEvent(self,event):
        #what to do if an object is dragged into the scene
        if config.drag_state:
            event.accept()

    #this method overrides the parent method
    def dragMoveEvent(self,event):
        if config.drag_state:
            event.accept()

    #this method overrides the parent method
    def dropEvent(self,event):
        if config.drag_state:
            event.accept()
        else:
            return

    def paintEvent(self, event):
        q = QPainter(self)
        config.drawLines(q)
