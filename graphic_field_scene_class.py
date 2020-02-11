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

class FieldGraphicsScene(QGraphicsScene):
    """this class provides a scene to manage items in the field"""

    #constructor
    def __init__(self,max_crops,max_animals):
        super().__init__()
        config.line_drawer = LineDrawer()
        self.field = Field(max_crops,max_animals)
        self.background_brush = QBrush()
        self.addWidget(config.line_drawer)

        config.line_drawer.resize(700, 1200) #fix to resize with resizing window
        #self.background_picture = QPixmap(":/field_background.png")
        #self.background_brush.setTexture(self.background_picture)
        #self.setBackgroundBrush(self.background_brush)

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

    def _visualise_graphic_item(self, type, name):
            x, y = self._drop_position(self.field._components[-1])
            current_view = self.views()[0]

            if type == "component":
                print(name)
                rect_item = QGraphicsRectItem(QtCore.QRectF(x - 50, y + 300, 100, 50))
            else:
                rect_item = QGraphicsRectItem(QtCore.QRectF(x - 50, y + 100, 500, 500))

            rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)
            config.sym_objects.append(rect_item)
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

        if event.mimeData().hasFormat("application/x-system"):
            system_added = self.field.add_component(SystemGraphicsPixmapItem())
            self._add_graphic_item(system_added, "system", "system")
        else:
            component_added = self.field.add_component(ComponentGraphicsPixmapItem())
            self._add_graphic_item(component_added, "component", event.mimeData().text())


    def paintEvent(self, event):
        q = QPainter(self)
        config.drawLines(q)
