import pygame
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, tamanho):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tamanho, tamanho))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
