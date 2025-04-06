from modules.utilities import Asset_Loader
from modules.gameobject import GameObject

class Background(GameObject):
    def __init__(self, image_path, speed = 1, pane_height = 100):
        super().__init__()
        self.speed = speed
        for i in range(3):
            pane = GameObject()
            pane.name = f"pane_{i}"
            pane.render_rect = False
            pane.render_image = True
            pane.image = Asset_Loader.load_image(image_path)
            pane.size.y = pane_height
            pane.size.x = self.engine.screen_size.x
            pane.position.x += self.engine.screen_size.x * i
            self.children.append(pane)
    def update(self):
        # move children
        self.position.x -= self.speed
        # loop
        if self.position.x <= -self.engine.screen_size.x:
            offset = self.position.x - -self.engine.screen_size.x
            self.position.x = 0 - offset
            