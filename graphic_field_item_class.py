from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QMenu

class FieldItemGraphicsPixmapItem(QGraphicsPixmapItem):
    """this class provides a pixmap item with a preset image for the item"""

    #constructor
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable) #allow us to move the graphic in the scene

    def update_status(self):
        pass
