import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
# NEIGHBOR_OFFSETS = [
#     (-2, -2), (1, -2), (0, -1), (1, -2), (2, -2),
#     (-2, -1), (1, -1), (0, -1), (1, -1), (2, -1),
#     (-2, 0), (1, 0), (0, 0), (1, 0), (2, 0),
#     (-2, 1), (1, 1), (0, 1), (1, 1), (2, 1),
#     (-2, 2), (1, 2), (0, 2), (1, 2), (2, 2)
# ]

PHYSICS_TILES = {'grass', 'stone'}  # a set for optimized lookups to see if something in a set is faster than in a list


class Tilemap:
    def __init__(self, game, tile_size=16):  # with game as argument
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(15):
            self.tilemap[str(3 + i) + ';20'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 20)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def tiles_around(self, pos):  # pos is an (x,y) tuple
        tiles = []
        # tile_loc is character's own position
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        # now we compare own pos to neighbors
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):  # pos is an (x,y) tuple
        rects = []  # empty list of rects that we apply physics on and return
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surf, offset=(0, 0)):
        # off grid tiles
        for tile in self.offgrid_tiles:
            # offset is a camera position
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # ON grid tiles
        for loc in self.tilemap:  # loc is 3;10 for example
            tile = self.tilemap[loc]  # this gives the values of a dictionary like {'type': 'grass',} and so on
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
            # ^ self.assets[tile['type']] - gives an array of images, [tile['variant']] - index of an image in that
            # array. tile['pos'][0] - 1st value in 'pos': tuple
