import pygame
import os

BASE_IMG_PATH = 'data/images'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()  # convert or convert_alpha every image
    # img = pygame.transform.scale(img, (int(40), int(40)))
    img.set_colorkey((0, 0, 0))  # so that black BG becomes transparent
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images
