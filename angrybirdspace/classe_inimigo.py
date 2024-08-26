import pygame
import numpy as np
import os

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, tamanho):
        pygame.sprite.Sprite.__init__(self)
        path = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(path, 'img', 'robot.png')
        self.image = pygame.image.load(caminho)
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
