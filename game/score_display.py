from modules.gameobject import GameObject
from modules.utilities import Asset_Loader
from modules.structs.vector import Vector2

digit_size = Vector2(24,36)

class Score_Display(GameObject):
    def __init__(self):
        super().__init__()
        self.render_rect = False
        self.render_image= False
        self.current_number = 0
        for i in range(3):
            digit = Digit()
            digit.position.x = digit_size.x * i
            self.children.append(digit)
        self.display_number(0)
    def display_number(self, number):
        if number > 999:
            raise Exception("Number too big")
        self.current_number = number
        padded_string = f'{number:0>3}'  # Pad with zeros to a width of 5
        for i in range(3):
            num = int(padded_string[i])
            self.children[i].set_digit(num)

class Digit(GameObject):
    def __init__(self):
        super().__init__()
        self.image_assets = []
        for i in range(10):
            image = Asset_Loader.load_image(f"{i}.png")
            self.image_assets.append(image)
        self.current_number = 0
        self.image = self.image_assets[self.current_number]
        self.render_rect = False
        self.render_image = True
        self.size = digit_size
    def set_digit(self, number):
        self.current_number = number
        self.image = self.image_assets[self.current_number]
        

