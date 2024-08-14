import pygame
import numpy as np
from classe_jogador import Bola  # Importa a classe Bola do arquivo bola.py
from classe_inimigo import Inimigo  # Importa a classe Inimigo do arquivo inimigo.py

class Game:
    def __init__(self):
        pygame.init()
        self.largura, self.altura = 1200, 800
        self.screen = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Angry Birds Space")
        self.clock = pygame.time.Clock()
        self.running = True

        # Configurações da bola
        self.bola = Bola(150, self.altura - 150, 15)
        self.arrastando = False
        self.controle_velocidade = 0.1

        # Criação de inimigos
        self.inimigos = pygame.sprite.Group()
        self.inimigos.add(Inimigo(600, self.altura - 100, 50))  # Adiciona um inimigo
        self.inimigos.add(Inimigo(800, self.altura - 200, 50))  # Adiciona outro inimigo

    def run(self):
        while self.running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    # Verifica se o clique do mouse está dentro da bola
                    if np.linalg.norm(np.array(evento.pos) - self.bola.pos) <= self.bola.raio:
                        self.arrastando = True
                        self.pos_inicial = self.bola.pos.copy()
                elif evento.type == pygame.MOUSEBUTTONUP:
                    if self.arrastando:
                        self.arrastando = False
                        destino = np.array(evento.pos, dtype=np.float64)
                        vetor_direcao = self.pos_inicial - destino
                        comprimento = np.linalg.norm(vetor_direcao)
                        if comprimento > 0:
                            vetor_direcao = vetor_direcao / comprimento  # Normaliza o vetor
                            self.bola.velocidade = vetor_direcao * comprimento * self.controle_velocidade
                            self.bola.lancamento = True
                elif evento.type == pygame.MOUSEMOTION and self.arrastando:
                    self.bola.pos = np.array(evento.pos, dtype=np.float64)

            self.bola.update(self.largura, self.altura)

            # Verifica colisão com inimigos
            for inimigo in self.inimigos:
                if pygame.sprite.collide_rect(self.bola, inimigo):
                    self.inimigos.remove(inimigo)
                    break  # Remove apenas um inimigo por vez

            self.screen.fill((0, 0, 0))
            self.bola.draw(self.screen)
            self.inimigos.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
