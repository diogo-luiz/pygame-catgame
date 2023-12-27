import pygame
from support import import_folder
from ui import UI

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        
        self.image = self.animations['idle'][self.frame_index]
        #center_x = x + 1 +int(64 / 2)
        #center_y = y + 1 + int(64 / 2)
        #self.rect = self.image.get_rect(topleft = (center_x,center_y))
        self.rect = self.image.get_rect(bottomleft = (pos))

        self.display_surface = surface
        self.ui = UI(self.display_surface)
        # Player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        

        self.teste = False
        self.status = 'idle'
        self.facing_right = False
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self): 
        character_path = 'graphics/character/'
        self.animations = {
            'idle':[],
            'run':[],
            'jump':[],
            'fall':[],
            'power':[],
            'power_idle':[],
            'power_fall':[],
            'power_jump':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            print(full_path)
            self.animations[animation] = import_folder(full_path)

            #self.animations[animation] = import_folder(full_path)

   
    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.facing_right:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
           
        else:
            self.image = image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
    
    

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0

        #jump
        if self.on_ground and keys[pygame.K_SPACE]:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            if self.teste:
                self.status = 'power_jump'
            else: self.status = 'jump'

        elif self.direction.y > 0.8:
            if self.teste:
                self.status = 'power_fall'
            else: self.status = 'fall'
            #    
        else:

            if self.direction.x != 0:
                if self.teste:
                    self.status = 'power'
                else:
                    self.status = 'run'
            else:
                if self.teste:   
                    self.status = 'power_idle'
                else:
                    self.status = 'idle'
                    

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        
