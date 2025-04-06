import pygame
from  modules.gameobject import GameObject
from modules.structs.vector import Vector2
from modules.utilities import Asset_Loader, map_range, lerp
from modules.sfx import SFX

# player constants
GRAV_SPEED = 1
GRAV_MAX = 10
INPUT_SPIKE = 20
MAX_SPEED = -10

class Player(GameObject):
    def __init__(self): 
        super().__init__()
        self.velocity = Vector2()
        self.rotation = 0
        self.name = "player"
        self.frame_count = 0
        self.frame_length = 3
        self.frame_index = 0
        self.max_frame_index = 2
        self.images = [
            Asset_Loader.load_image("yellowbird-downflap.png"),
            Asset_Loader.load_image("yellowbird-midflap.png"),
            Asset_Loader.load_image("yellowbird-upflap.png")
        ]
        # events
        self.on_player_collide_with_pipe = None
        self.on_player_collide_with_gap= None
    def update(self):
        # animation
        self.animate_loop()
        # check collisions
        if len(self.current_collisions) > 0:
            other_obj = self.current_collisions[0]
            if other_obj.name == "gap":
                if self.on_player_collide_with_pipe != None:
                    self.on_player_collide_with_gap()
            else:
                if self.on_player_collide_with_pipe != None:
                    self.on_player_collide_with_pipe()
        # handle velocity
        self.velocity.y += GRAV_SPEED # gravity speed
        # clamp velocity
        if self.velocity.y > GRAV_MAX:
            self.velocity.y = GRAV_MAX
        # update position based on velocity
        self.position += self.velocity
        # handle roation of the flappy bird
        target_rotation = map_range(
            self.velocity.y,
            -10,
            10,
            30,
            -30
        )
        self.rotation = lerp(self.rotation, target_rotation, 0.3)
        self.image = pygame.transform.rotate(self.image, self.rotation)
    def input_pressed(self):
        SFX.play("wing")
        # spike velocity up
        self.velocity.y -= INPUT_SPIKE
        # clamp velocity
        if self.velocity.y < MAX_SPEED:
            self.velocity.y = MAX_SPEED
    def animate_loop(self):
        # count frame
        self.frame_count += 1
        # check if should be next frmae
        if(self.frame_count > self.frame_length):
            # reset count
            self.frame_count = 0
            # increment frame index
            self.frame_index += 1
            # cycle frame index if need be
            if(self.frame_index > self.max_frame_index):
                self.frame_index = 0
        # set the current image
        self.image = pygame.transform.scale(self.images[self.frame_index], self.size.to_tuple())
        
        