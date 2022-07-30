import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size
from tile import Tile, StaticTile, Crate, AnimatedTile, Coin, Palm
from enemy import Enemy


class Level:
    def __init__(self, level_data, surface):
        # General setup
        self.display_surface = surface
        self.world_shift = -4

        # Enemy
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Grass setup
        grass_layout = import_csv_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")

        # Crates
        crate_layout = import_csv_layout(level_data["crates"])
        self.crate_sprites = self.create_tile_group(crate_layout, "crates")

        # Coins
        coin_layout = import_csv_layout(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # Foreground palms
        fg_palm_layout = import_csv_layout(level_data["fg_palms"])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg_palms')

        # Background palms
        bg_palm_layout = import_csv_layout(level_data["bg_palms"])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg_palms')

        # Enemy
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # Constraint
        constraint_layout = import_csv_layout(level_data["constraints"])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        terrain_tile_list = import_cut_graphics("./graphics/terrain/terrain_tiles.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "grass":
                        grass_tile_list = import_cut_graphics("./graphics/decoration/grass/grass.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "crates":
                        sprite = Crate(tile_size, x, y)

                    if type == "coins":
                        if val == "0":
                            sprite = Coin(tile_size, x, y, "./graphics/coins/gold")
                        else:
                            sprite = Coin(tile_size, x, y, "./graphics/coins/silver")

                    if type == "fg_palms":
                        if val == "0":
                            sprite = Palm(tile_size, x, y, "graphics/terrain/palm_small", 38)
                        if val == "1":
                            sprite = Palm(tile_size, x, y, "graphics/terrain/palm_large", 64)

                    if type == "bg_palms":
                        sprite = Palm(tile_size, x, y, "graphics/terrain/palm_bg", 64)

                    if type == "enemies":
                        sprite = Enemy(tile_size, x, y)

                    if type == "constraints":
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self, player_setup):
        for row_index, row in enumerate(player_setup):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0":
                    print("player goes here")
                if val == "1":
                    hat_surface = pygame.image.load("./graphics/character/hat.png").convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):
        # Run entire level
        # Background palms
        self.bg_palm_sprites.draw(self.display_surface)
        self.bg_palm_sprites.update(self.world_shift)

        # Terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # Enemies
        self.enemy_sprites.draw(self.display_surface)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.update(self.world_shift)

        # Crates
        self.crate_sprites.draw(self.display_surface)
        self.crate_sprites.update(self.world_shift)

        # Grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # Coins
        self.coin_sprites.draw(self.display_surface)
        self.coin_sprites.update(self.world_shift)

        # Foreground palms
        self.fg_palm_sprites.draw(self.display_surface)
        self.fg_palm_sprites.update(self.world_shift)

        # Player sprite
        self.goal.draw(self.display_surface)
        self.goal.update(self.world_shift)