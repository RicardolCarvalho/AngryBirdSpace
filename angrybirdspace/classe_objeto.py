import pygame
import os

class Objeto(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        pygame.sprite.Sprite.__init__(self)
        path = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(path, 'img', 'caixa.png')
        self.image = pygame.image.load(caminho_imagem)
        self.image = pygame.transform.scale(self.image, (largura, altura))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)