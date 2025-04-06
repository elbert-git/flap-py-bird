import sys
import pygame
from .structs.vector import Vector2
from modules.gameobject import GameObject

class Engine:
    # Game properties
    fps:int = 60
    screen_scale = 40
    screen_size:Vector2 = Vector2(9*screen_scale, 16*screen_scale)

    # state
    prev_time = 0
    delta_time = 0

    # run bool
    running = True

    # references
    objects:list[GameObject] = []

    @classmethod
    def initialize(cls):
        # init pygame
        pygame.init()
        # setup pygame references
        cls.screen = pygame.display.set_mode((cls.screen_size.x, cls.screen_size.y))
        cls.clock = pygame.time.Clock()
        # set the display caption
        pygame.display.set_caption("Flap PY Bird")
    
    @classmethod
    def start(cls):
        # start loop
        while cls.running:
            cls.loop()
            cls.render()

    @classmethod
    def loop(cls):
        # handling delta time
        current_time = pygame.time.get_ticks()
        cls.delta_time = current_time - cls.prev_time
        cls.prev_time = current_time
        
        # event handler
        for event in pygame.event.get():
            # detect quit event
            if event.type == pygame.QUIT:
                cls.running = False
                cls.quit_app()
            # detect input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Check if the spacebar is pressed
                    for o in cls.objects:
                        o.input_pressed()

        # update all objects
        for obj in cls.objects:
            obj.internal_update()
        # limit fps
        cls.clock.tick(cls.fps)
        
    @classmethod
    def render(cls):
        # clear screen
        cls.screen.fill((0,0,0))

        # render objects
        for obj in cls.objects:
            obj.internal_render()

        # update the screen
        pygame.display.update()
    
    @classmethod
    def quit_app(cls):
        pygame.quit()
        sys.exit()
        
        


    
    