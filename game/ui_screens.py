from modules.gameobject import GameObject
from modules.utilities import Asset_Loader
from modules.structs.vector import Vector2

class UI_Overlay(GameObject):
    def __init__(self, image_path):
        super().__init__()
        # handle self
        self.size = self.engine.screen_size
        self.rect_color = (0,0,0)
        self.render_rect = True
        # create child
        element = GameObject()
        self.children.append(element)
        element.image = Asset_Loader.load_image(image_path)
        element.render_image = True
        element.render_rect = False
        element.position = Vector2(
            (self.engine.screen_size.x /2) - element.image.get_width()/2,
            (self.engine.screen_size.y /2) - element.image.get_height()/2
        )
        element.size = Vector2(
            element.image.get_width(),
            element.image.get_height()
        )
        # event
        self.on_input_received = None
    def input_pressed(self):
        if self.active:
            if self.on_input_received != None:
                self.on_input_received()
        
