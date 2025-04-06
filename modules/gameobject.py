import pygame
from .structs.vector import Vector2

class GameObject:
    count:int = 0;
    all_objects:list = []
    def __init__(self, name="some game object", image=None):
        # assign id
        GameObject.count += 1
        self.id = GameObject.count
        # states
        self.current_collisions:list[GameObject] = []
        self.previous_collided_id = None
        # tranform states
        self.global_offset = Vector2()
        self.position:Vector2 = Vector2()
        self.size:Vector2 = Vector2(10, 10)
        # create rect
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        # properties
        self.name:string = name
        self.rect_color = (255,255,255)
        self.is_checking_for_collisions:bool = False
        self.can_be_collided:bool = False
        self.render_rect = False
        self.render_image = False
        self.visible = True
        self.active = True
        # references
        self.image = image
        self.children:list[GameObject] = []
        from modules.engine import Engine
        self.engine:Engine = Engine
        self.screen = self.engine.screen
        # append to class array
        GameObject.all_objects.append(self)
   
    # * --- main functions 
    # updates
    def internal_update(self, offset_pos=Vector2(), offset_size=Vector2(1, 1)):
        if self.active:
            # get global position
            global_position = offset_pos + self.position
            global_size = offset_size.multiply_with_vector(self.size)
            self.global_offset = offset_pos
            # update game rect position 
            self.rect.x = global_position.x
            self.rect.y = global_position.y
            self.rect.width = global_size.x
            self.rect.height = global_size.y
            # scale image
            if self.image != None:
                self.image = pygame.transform.scale(self.image, self.size.to_tuple())
            # collisions check
            if self.is_checking_for_collisions:
                self.check_collisions()
            # main update
            self.update()
            # update children
            for i in self.children:
                i.internal_update(global_position)
    def update(self):
        pass
        # print("default GameObject update")
    # renders
    def internal_render(self):
        if self.visible:
            # render self
            self.render_to_screen()
            # render children
            for obj in self.children:
                obj.internal_render()
    def render_to_screen(self):
        # render rect
        if self.render_rect:
            pygame.draw.rect(self.screen, self.rect_color, self.rect)
        # render image
        if self.render_image:
            if self.image != None:
                self.engine.screen.blit(self.image, (self.position+self.global_offset).to_tuple())

    # * --- input handling
    def input_pressed(self):
        # print("GameObject received input")
        pass
    
    def check_collisions(self):
        # clear previous frame collisions
        self.current_collisions = [] 
        # check for collisionts
        for other_obj in GameObject.all_objects: # for every obj
            if self.id != other_obj.id: # dont collide with self
                if other_obj.active:
                    if other_obj.can_be_collided: # only collide with collidables
                        if self.rect.colliderect(other_obj.rect): # if colliding
                            if other_obj.id != self.previous_collided_id:
                                self.current_collisions.append(other_obj) # add to object
                                self.previous_collided_id = other_obj.id
    
    def __str__(self):
        return f"<gameobject>: {self.name}"
    def __repr__(self):
        return f"<gameobject>: {self.name}"
                    

            