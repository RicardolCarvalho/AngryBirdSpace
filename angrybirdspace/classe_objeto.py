import pygame

class Objeto(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, cor=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((largura, altura))
        self.image.fill(cor)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)