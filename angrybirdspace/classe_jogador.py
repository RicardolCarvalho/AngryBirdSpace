import pygame
import numpy as np

class Bola(pygame.sprite.Sprite):
    def __init__(self, x, y, raio):
        pygame.sprite.Sprite.__init__(self)
        self.raio = raio
        self.image = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (raio, raio), raio)
        self.rect = self.image.get_rect(center=(x, y))
        self.inicial_pos = np.array([x, y], dtype=np.float64)
        self.pos = self.inicial_pos.copy()
        self.lancamento = False
        self.velocidade = np.zeros(2, dtype=np.float64)
        self.gravidade = np.array([0, 0.1], dtype=np.float64)

    def draw(self, screen):
        rect = pygame.Rect(self.pos - self.raio, (self.raio * 2, self.raio * 2))
        screen.blit(self.image, rect.topleft)

    def update(self, largura, altura):
        if self.lancamento:
            self.velocidade += self.gravidade
            self.pos += self.velocidade

            # Resetar se sair da tela
            if (self.pos[0] < 0 or self.pos[0] > largura or
                    self.pos[1] < 0 or self.pos[1] > altura):
                self.resetar()

            # Atualiza a posição do retângulo de colisão
            self.rect.center = self.pos

    def resetar(self):
        self.pos = self.inicial_pos.copy()
        self.velocidade = np.zeros(2, dtype=np.float64)
        self.lancamento = False
