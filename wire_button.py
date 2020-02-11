import config
from graphic_field_scene_class import *

def wire_button_pressed():
    config.drag_state = not config.drag_state
    config.draw_wire_state = not config.draw_wire_state
    config.setDragState()
