import pygame
import random
from settings import *
import sys
from pygame import mixer

mixer.init()

# Sound FX
hit_fx = pygame.mixer.Sound('hit.mp3')
hit_fx.set_volume(0.3)


class Ninja(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.velocity = [0, 0]  # velocity list
        self.image = pygame.image.load('nin_idle1.png')
        self.jump_image = pygame.image.load('nin_jump1.png')
        self.image.set_colorkey((0, 0, 0))
        self.jump_image.set_colorkey((0, 0, 0))
        self.scale = 2
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.idle_image = self.image
        self.jump_image = pygame.transform.scale(self.jump_image, (
            int(self.jump_image.get_width() * self.scale), int(self.jump_image.get_height() * self.scale)))
        # Get the rectangular area of the ninja's image
        self.rect = self.image.get_frect()
        # Set the initial position of the ninja
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - NINJA_HEIGHT - 200)
        self.is_jumping = False
        self.attacking = False
        self.flip = False
        self.direction_left = False  # Used to determine which way the ninja is facing
        self.sword_rect = pygame.FRect(0, 0, 0, 0)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def update(self, platforms, enemies, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        keys = pygame.key.get_pressed()
        # Movement
        if keys[pygame.K_PERIOD] and not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = -JUMP_STRENGTH
            self.image = self.jump_image

        frame_movement = (movement[0] * MOVE_SPEED + self.velocity[0], movement[1] + self.velocity[1])
        self.rect.x += frame_movement[0]  # X position
        for tile_rect in tilemap.physics_rects_around((self.rect.x, self.rect.y)):
            if self.rect.colliderect(tile_rect):
                if frame_movement[0] > 0:
                    self.rect.right = tile_rect.left
                    self.collisions['right'] = True
                    print("collisions['right']")
                if frame_movement[0] < 0:
                    self.rect.left = tile_rect.right
                    self.collisions['left'] = True
                    print("collisions['left']")

        self.rect.y += frame_movement[1]  # Y position
        for tile_rect in tilemap.physics_rects_around((self.rect.x, self.rect.y)):
            if self.rect.colliderect(tile_rect) and self.velocity[1] > 0:
                if frame_movement[1] > 0:
                    self.is_jumping = False
                    self.rect.bottom = tile_rect.top
                    self.collisions['down'] = True
                    print("collisions['down']")
                    self.image = self.idle_image
                    self.velocity[1] = 0
                if frame_movement[1] < 0:
                    self.rect.top = tile_rect.bottom
                    self.collisions['up'] = True
                    print("collisions['up']")

        # Apply gravity
        self.velocity[1] += GRAVITY

        # Check for collisions with platforms
        entity_rect = self.rect
        for platform in platforms:
            # If collision with platform while falling
            if self.rect.colliderect(platform) and self.velocity[1] > 0:
                self.rect.bottom = platform.top  # Set ninja's bottom to top of platform
                self.is_jumping = False
                self.image = self.idle_image
                self.velocity[1] = 0

        # Check for sword collisions
        self.sword_collides_with_enemy(enemies)

    def draw(self, screen, offset=(0, 0)):
        # Draw the ninja on the screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - offset[0], self.rect.y - offset[1]))
        if self.attacking:
            # Determine sword position based on direction
            if not self.direction_left:  # Facing right
                sword_rect = pygame.FRect(self.rect.right, self.rect.centery - 10 - SWORD_HEIGHT / 2, SWORD_WIDTH,
                                         SWORD_HEIGHT)
            else:  # Facing left
                sword_rect = pygame.FRect(self.rect.left - SWORD_WIDTH, self.rect.centery - 10 - SWORD_HEIGHT / 2,
                                         SWORD_WIDTH, SWORD_HEIGHT)
            pygame.draw.rect(screen, SWORD_COLOR, sword_rect)

    def sword_collides_with_enemy(self, enemies):
        sword_rect = pygame.FRect(0, 0, 0, 0)
        if self.attacking:
            if not self.direction_left:  # Facing right
                sword_rect = pygame.FRect(self.rect.right, self.rect.centery - 10 - SWORD_HEIGHT / 2, SWORD_WIDTH,
                                         SWORD_HEIGHT)
            else:  # Facing left
                sword_rect = pygame.FRect(self.rect.left - SWORD_WIDTH, self.rect.centery - 10 - SWORD_HEIGHT / 2,
                                         SWORD_WIDTH, SWORD_HEIGHT)

            # Check for collisions
            for enemy in enemies.array:
                if sword_rect.colliderect(enemy):
                    hit_fx.play()
                    enemies.array.remove(enemy)  # Remove enemy if collision detected


class Enemy:
    def __init__(self, surf):
        self.width = 10
        self.surf = surf
        self.height = 20
        self.array = []  # List to store enemy rectangles
        self.color = (0, 118, 119)  # ENEMY COLOR

    def render(self, x, y, offset=(0, 0)):
        # Draws a red rectangle representing an enemy
        pygame.draw.rect(self.surf, self.color, (x - offset[0], y - offset[1], self.width, self.height))

    def update(self):
        if random.randint(1, 50) == 1:  # 2% chance to spawn an enemy each frame
            enemy_x = random.randint(0, int(SCREEN_WIDTH) - self.width)
            enemy_rect = pygame.FRect(enemy_x, 0, self.width, self.height)

            self.array.append(enemy_rect)

        # Move enemies
        for enemy in self.array:
            enemy.y += 2  # Move enemies down
            if enemy.y > SCREEN_HEIGHT:  # Remove enemies that go off-screen
                self.array.remove(enemy)
