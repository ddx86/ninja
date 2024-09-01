"""
pygame.rect(*self.img_pos, *self.img.get_size()) # to not write 4 arguments
"""

import pygame
import sys
from utils import load_image, load_images
from entities3 import Ninja, Enemy
from tilemap import Tilemap
from settings import *
from pygame import mixer


class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        mixer.init()
        pygame.display.set_caption("Nindo")  # Sets the title of the game window

        # # Music
        # pygame.mixer.music.load('nin_music.mp3')
        # pygame.mixer.music.set_volume(0.3)
        # pygame.mixer.music.play(-1, 40.0, 5000)

        # Create the screen, clock, and set the title
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creates the game window
        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # FULLSCREEN VERISON

        self.clock = pygame.time.Clock()  # Used to control the game's frame rate

        self.movement = [False, False]  # movement of a player in [x,y]

        self.player = Ninja(self)  # Create the ninja object
        self.enemies = Enemy(self.display)  # Create enemy object

        self.platforms = []
        self.platforms.append(pygame.FRect(0, (SCREEN_HEIGHT - 50), SCREEN_WIDTH, 50))
        self.platforms.append(pygame.FRect(200, 400, 200, 20))
        self.platforms.append(pygame.FRect(100, 160, 20, 20))
        self.platforms.append(pygame.FRect(400, 160, 20, 20))
        self.platforms.append(pygame.FRect(500, 300, 200, 20))

        self.all_sprites = pygame.sprite.Group()  # Create a group to hold all sprites (ninja and platforms)

        # Assets
        self.assets = {
            'decor': load_images('/tiles/decor'),
            'grass': load_images('/tiles/grass'),
            'large_decor': load_images('/tiles/large_decor'),
            'stone': load_images('/tiles/stone'),
            'player': load_image('/entities/player.png')
        }

        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

    # Main Game Loop
    def run(self):
        running = True
        while running:  # Main game loop

            self.all_sprites.update(self.platforms, self.enemies)  # Update all sprites (platforms, enemies)
            # PLAYER UPDATE
            self.player.update(self.platforms, self.enemies, self.tilemap, (self.movement[1] - self.movement[0], 0))

            self.display.fill(SCREEN_COLOR)  # Fill the screen with white
            self.tilemap.render(self.display, offset=self.scroll)

            for platform in self.platforms:
                pygame.draw.rect(self.display, PLATFORM_COLOR, platform)

            self.player.draw(self.display, offset=self.scroll)  # Draw the ninja (including the sword if attacking)

            # Spawn enemies
            self.enemies.update()

            # Drawing enemies:
            for e in self.enemies.array:
                self.enemies.render(e[0], e[1], offset=self.scroll)  # Draw all enemies

            # Handling keyboard.
            for event in pygame.event.get():  # Handle events
                if event.type == pygame.QUIT:  # If the user clicks the close button
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and self.player.rect.x > 0:
                        self.movement[0] = True
                        self.player.direction_left = True
                        self.player.flip = True
                    if event.key == pygame.K_d and self.player.rect.x < SCREEN_WIDTH - self.player.image.get_width():
                        self.movement[1] = True
                        self.player.direction_left = False
                        self.player.flip = False
                    if event.key == pygame.K_COMMA:  # Attack if 'x' key is pressed
                        self.player.attacking = True

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_COMMA:
                        self.player.attacking = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        pygame.quit()  # Quit Pygame
        sys.exit()  # Exit the program


if __name__ == '__main__':
    game = Game()
    game.run()
