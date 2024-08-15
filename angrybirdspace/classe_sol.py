import pygame
import numpy as np

class Sol(pygame.sprite.Sprite):
    def __init__(self, posicao, raio=10):
        self.posicao = np.array(posicao, dtype=np.float64)
        self.forca_atracao = 1000
        self.raio = raio

    def aplicar_forca(self, bola):
        vetor = self.posicao - bola.pos
        distancia = np.linalg.norm(vetor)

        if distancia > 0:
            aceleracao = (self.forca_atracao / distancia**2) * (vetor / distancia)
            bola.velocidade += aceleracao

    def draw(self, tela):
        pygame.draw.circle(tela, (102, 102, 102), self.posicao.astype(int), self.raio)
