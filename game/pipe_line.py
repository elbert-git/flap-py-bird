from modules.gameobject import GameObject
from modules.utilities import Asset_Loader
from modules.structs.vector import Vector2
import pygame
import random

class Pipe_Line_Manager(GameObject):
    def __init__(self, pool_size = 10):
        super().__init__()
        self.render_rect = False
        # properties
        self.time_count = 0
        self.spawn_interval = 4 * 1000 # in seconds
        # create n number of pipes
        for i in range(pool_size):
            pipeline = Pipe_Line(gap_height= 150)
            pipeline.active = False
            pipeline.visible = False
            self.children.append(pipeline)
        # deactivate all of them
    def reset_and_initialise(self):
        pass
        # for all pipes, make them invisible, and reset position
    def update(self):
        # handle time stuff
        self.time_count += self.engine.delta_time
        if(self.time_count > self.spawn_interval):
            self.spawn_pipe()
            self.time_count = 0
    def spawn_pipe(self):
        # get available pipe
        current_pipe = None
        for pipe in self.children:
            if pipe.active == False:
                current_pipe = pipe
                break
        # if available spawn at the edge of the screen with some random positions
        if current_pipe != None:
            # activate pipe
            current_pipe.active = True
            current_pipe.visible = True
            # position pipe
            current_pipe.position.x = self.engine.screen_size.x * 1.5 # spawn half screen away from ledge
            current_pipe.position.y = self.engine.screen_size.y/2 + random.uniform(-50.0, 50.0)
            current_pipe.set_gap_height(random.uniform(200.0, 300.0))
    def reset(self):
        for pipe in self.children:
            # disable all pipes
            pipe.active = False
            pipe.visible = False
            # move off screen
            pipe.position.x = self.engine.screen_size.x * 1.5 # spawn half screen away from ledge
            pipe.position.y = self.engine.screen_size.y/2 + random.uniform(-50.0, 50.0)
            # ! lol very shoddy implementation but it will work
            # force to update rect positions to prevent collisions with previous position
            pipe.active = True
            pipe.internal_update()
            pipe.active = False
        
        


class Pipe_Line(GameObject):
    def __init__(self, gap_height=150):
        super().__init__()
        # --- key properties
        # name
        self.name = "pipe_line"
        # positioning the pipes
        self.gap_height = gap_height
        self.pipe_height = 300
        self.pipe_width = 90
        self.gap_width = 10
        # movement
        self.speed = 1.5
        # --- create children
        self.top_pipe = GameObject("pipe")
        self.bottom_pipe = GameObject("pipe")
        self.gap_rect = GameObject("gap")
        self.top_pipe.can_be_collided = True
        self.bottom_pipe.can_be_collided = True
        self.gap_rect.can_be_collided = True
        self.children.append(self.top_pipe)
        self.children.append(self.bottom_pipe)
        self.children.append(self.gap_rect)
        # --- position and scale children
        self.set_gap_height(gap_height)
        # --- color the pipes
        self.top_pipe.rect_color = (0,255,0)
        self.bottom_pipe.rect_color = (0,255,0)
        self.gap_rect.rect_color = (0,0,255)
        # load the image
        self.bottom_pipe.image = Asset_Loader.load_image("pipe-green.png")
        self.bottom_pipe.render_rect = False
        self.bottom_pipe.render_image = True
        self.top_pipe.image = Asset_Loader.load_image("pipe-green-flip.png")
        self.top_pipe.render_rect = False
        self.top_pipe.render_image = True
        # handle rect and image visiibilities
        self.render_rect = False
        self.bottom_pipe.render_rect = False
        self.gap_rect.render_rect = False
        self.top_pipe.render_rect = False
    def update(self):
        # move the pipe
        self.position.x -= self.speed
        # if position reaches other side of screen: disable it
        if self.position.x < -(self.engine.screen_size.x/2): # if half screen away from left side
            self.active = False
            self.visible = False
    def set_gap_height(self, gap_height):
        self.gap_height = gap_height
        self.top_pipe.position = Vector2()
        self.bottom_pipe.position = Vector2()
        self.gap_rect.position = Vector2()
        self.top_pipe.position.y -= (self.gap_height/2) + self.pipe_height
        self.top_pipe.position.x -= (self.pipe_width/2) - (self.gap_width/2)
        self.top_pipe.size.y = self.pipe_height
        self.top_pipe.size.x = self.pipe_width
        self.bottom_pipe.position.y += (self.gap_height/2) 
        self.bottom_pipe.position.x -= (self.pipe_width/2) - (self.gap_width/2)
        self.bottom_pipe.size.y = self.pipe_height
        self.bottom_pipe.size.x = self.pipe_width
        self.gap_rect.position.y -= (self.gap_height/2)
        self.gap_rect.size.y = self.gap_height
        self.gap_rect.size.x = self.gap_width


class Pipe(GameObject):
    def __init__(self):
        super().__init__()
        self.rect_color = (0,255,0)
    
    