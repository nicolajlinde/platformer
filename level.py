import pygame
from support import import_csv_layout
from settings import tile_size
from tile import Tile


class Level:
    def __init__(self, level_data, surface):
        # General setup
        self.display_surface = surface
        self.world_shift = -1

        # Terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        sprite = Tile(tile_size, x, y)
                        sprite_group.add(sprite)
        return sprite_group

    def run(self):
        # Run entire level
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
