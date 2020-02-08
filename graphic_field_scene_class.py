try:
    from PyQt4.QtGui import *
except:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *

from field_class import *
from graphic_system_item_class import *
from PyQt5 import QtCore


class FieldGraphicsScene(QGraphicsScene):
    """this class provides a scene to manage items in the field"""

    #constructor
    def __init__(self,max_crops,max_animals):
        super().__init__()

        self.field = Field(max_crops,max_animals)

        self.background_brush = QBrush()
        #self.background_picture = QPixmap(":/field_background.png")
        #self.background_brush.setTexture(self.background_picture)
        #self.setBackgroundBrush(self.background_brush)

    def _drop_position(self,item):
        cursor_position = QCursor.pos() #global cursor position
        current_view = self.views()[0]
        scene_position = current_view.mapFromGlobal(cursor_position)

        width = item.boundingRect().width()
        height = item.boundingRect().height()

        width_offset = width/2
        height_offset = height/2

        drop_x = scene_position.x() - width_offset
        drop_y = scene_position.y() - height_offset

        return drop_x, drop_y

    def _visualise_graphic_item(self, type, name):
            if type == "component":
                print(name)
                x, y = self._drop_position(self.field._components[-1])
                current_view = self.views()[0]
                rect_item = QGraphicsRectItem(QtCore.QRectF(x, y, 100, 50))
                rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
                self.addItem(rect_item)
            else:
                x, y = self._drop_position(self.field._components[-1])
                current_view = self.views()[0]
                rect_item = QGraphicsRectItem(QtCore.QRectF(x, y, 500, 500))
                rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
                self.addItem(rect_item)

    def _add_graphic_item(self,result, type, name):
        if result:
            self._visualise_graphic_item(type, name)
        else:
            error_message = QMessageBox()
            error_message.setText("No more {0}s can be added to this field".format(graphic_item_type))
            error_message.exec()

    #this method overrides the parent method
    def dragEnterEvent(self,event):
        #what to do if an object is dragged into the scene
        event.accept()

    #this method overrides the parent method
    def dragMoveEvent(self,event):
        event.accept()

    #this method overrides the parent method
    def dropEvent(self,event):
        event.accept()
        #what to do if an object is dropped on the scene
        if event.mimeData().hasFormat("application/x-system"):
            system_added = self.field.add_component(SystemGraphicsPixmapItem())
            self._add_graphic_item(system_added, "system", "system")
        else:
            component_added = self.field.add_component(ComponentGraphicsPixmapItem())
            self._add_graphic_item(component_added, "component", event.mimeData().text())
