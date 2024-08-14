import pygame
import numpy as np
from classe_jogador import Bola
from classe_inimigo import Inimigo
from classe_menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.largura, self.altura = 1200, 700
        self.screen = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Angry Birds Space")
        self.clock = pygame.time.Clock()
        self.running = True

        self.bola = Bola(150, self.altura - 150, 15)
        self.arrastando = False
        self.controle_velocidade = 0.1

        self.inimigos = pygame.sprite.Group()
        self.inimigos.add(Inimigo(600, self.altura - 100, 50))
        self.inimigos.add(Inimigo(900, self.altura - 200, 50))

        self.menu = Menu()
        self.menu.mostrar = True
        
    def run(self):
        while self.running:
            if self.menu.mostrar:
                self.menu.draw(self.screen)
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.running = False
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        acao = self.menu.checar_clique(evento.pos)
                        if acao == 'comecar':
                            self.menu.mostrar = False
            else:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.running = False
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
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
                                vetor_direcao = vetor_direcao / comprimento
                                self.bola.velocidade = vetor_direcao * comprimento * self.controle_velocidade
                                self.bola.lancamento = True
                    elif evento.type == pygame.MOUSEMOTION and self.arrastando:
                        self.bola.pos = np.array(evento.pos, dtype=np.float64)

                self.bola.update(self.largura, self.altura)

                for inimigo in self.inimigos:
                    if pygame.sprite.collide_rect(self.bola, inimigo):
                        self.inimigos.remove(inimigo)
                        break

                self.screen.fill((0, 0, 0))
                self.bola.draw(self.screen)
                self.inimigos.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
