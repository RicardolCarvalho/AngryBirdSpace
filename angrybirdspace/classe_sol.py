import pygame
import numpy as np
import os



class Sol(pygame.sprite.Sprite):
    def __init__(self, posicao, raio=50):
        pygame.sprite.Sprite.__init__(self)
        path = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(path,'img', 'sol.webp')
        self.image = pygame.image.load(caminho)
        self.image = pygame.transform.scale(self.image, (raio, raio))
        self.posicao = np.array(posicao, dtype=np.float64)
        self.forca_atracao = 5000
        self.raio = raio

    def aplicar_forca(self, bola):
        vetor = self.posicao - bola.pos
        distancia = np.linalg.norm(vetor)

        if distancia > 0:
            aceleracao = (self.forca_atracao / (distancia**2)) * (vetor / distancia)
            bola.velocidade += aceleracao


    def draw(self, tela):
        tela.blit(self.image, self.posicao - self.raio)
        # pygame.draw.circle(tela, (102, 102, 102), self.posicao.astype(int), self.raio)