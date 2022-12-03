import pygame
import os

class Background:
    def __init__(self):
        self.image_list = []
        self.images_width = []
        self.n = 0
        self.offset = 0

    def load_images(self):
        for file in os.listdir('background/'):
            image = pygame.image.load(f"background/{file}")
            rect = image.get_rect()
            largeur = rect.width
            self.image_list.append(image)
            self.images_width.append(largeur)

    def update_background(self, screen):
        image1 = self.image_list[self.n]
        image2 = self.image_list[self.n + 1]
        largeur1 = self.images_width[self.n]
        screen.blit(image1, (self.offset, 0))
        screen.blit(image2, (self.offset + largeur1, 0))
        self.offset -= 2
        if abs(self.offset) >= largeur1:
            self.n += 1
            self.offset = 0
        if self.n == len(self.image_list)-1:
            self.n = 0