import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height, screen_width
from Tiles import Tile, StaticTile, Crate, Coin, Palm, Whiska
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from ui import UI

class Level:
    def __init__(self,level_data,surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.ui = UI(self.display_surface)
        self.ativo = False

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Whiska setup
        whiska_layout = import_csv_layout(level_data['whiska'])
        self.whiska_sprite = self.create_tile_group(whiska_layout,'whiska')


        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprite = self.create_tile_group(terrain_layout,'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout,'crates')

        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprite = self.create_tile_group(coin_layout,'coins')

        # fg palmtree
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')
        # bg palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')
    
        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprite = self.create_tile_group(enemy_layout,'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) *tile_size
        self.water = Water(screen_height - 20, level_width)
        self.clouds = Clouds(400,level_width,30)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        sprite_group.add(sprite)
                    if type == 'grass':
                        grass_tile_list = import_cut_graphic('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'crates':
                        sprite = Crate(tile_size,x,y)
                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size,x,y,'graphics/coins/gold')
                        if val == '1': sprite = Coin(tile_size,x,y,'graphics/coins/silver')
                    if type == 'fg palms':
                        if val == '0': sprite = Palm(tile_size,x,y,'graphics/terrain/palm_small',38)
                        if val == '1': sprite = Palm(tile_size,x,y,'graphics/terrain/palm_large',64)
                    if type == 'bg palms':
                        sprite = Palm(tile_size,x,y,'graphics/terrain/palm_bg',64)
                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)
                    if type == 'whiska':
                        sprite = Whiska(tile_size,x,y,'graphics/whiska')
                    
                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)

                    
        return sprite_group
        

    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if val == '0':
                    sprite = Player((x,y),self.display_surface)
                    self.player.add(sprite)
                    if self.player.sprite.direction.y >= 90:
                        self.player.sprite.direction.y
                if val == '1':
                    hat_surface = pygame.image.load('graphics/character/hat.png')
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprite.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()
    
    def horizontal_movement_collision(self):
            player = self.player.sprite
            player.rect.x += player.direction.x * player.speed
            
            collidable_sprites = self.terrain_sprite.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
            for sprite in collidable_sprites:
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                        player.on_left = True
                        self.current_x = player.rect.left
                    
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                        player.on_right = True
                        self.current_x = player.rect.right

            whiska_collide = self.whiska_sprite.sprites()
            for collision in whiska_collide:
                keys = pygame.key.get_pressed()

                if collision.rect.colliderect(player.rect):
                    self.ativo = True
                    if keys[pygame.K_e]:
                        player.teste = True
                        self.ativo = False
                       
            
            if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprite.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_x < (screen_width / 2) + 32 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - ((screen_width /2) + 2) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):
        

        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)
        # bg palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        self.terrain_sprite.draw(self.display_surface)
        

        # enemy
        self.enemy_sprite.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprite.draw(self.display_surface)
        
        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # coins
        self.coin_sprite.update(self.world_shift)
        self.coin_sprite.draw(self.display_surface)

        #whiskas
        self.whiska_sprite.draw(self.display_surface)
        self.whiska_sprite.update(self.world_shift)

        # fg palm
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # player sprite
        self.player.update()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.goal.draw(self.display_surface)

        #water
        self.water.draw(self.display_surface,self.world_shift)
        if self.ativo:
            self.ui.show_interact()





