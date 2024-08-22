import pygame
import numpy as np
import os
from angrybirdspace.classe_jogador import Bola
from angrybirdspace.classe_inimigo import Inimigo
from angrybirdspace.classe_menu import Menu
from angrybirdspace.classe_objeto import Objeto
from angrybirdspace.classe_sol import Sol

class Game:
    def __init__(self):
        pygame.init()
        self.largura, self.altura = 1200, 700
        self.screen = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Angry Birds Space")
        self.clock = pygame.time.Clock()
        self.running = True

        # Fundo do jogo
        caminho = os.path.join('angrybirdspace', 'img', 'espaco.webp')
        print(caminho)
        self.fundo = pygame.image.load(caminho)
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
 
        # Bola
        self.bola = Bola(150, self.altura - 150, 30)
        self.arrastando = False
        self.controle_velocidade = 0.1

        # Inimigos
        self.inimigos = pygame.sprite.Group()
        self.inimigos.add(Inimigo(1100, 565, 50))
        self.inimigos.add(Inimigo(725, 65, 50))

        # Objetos
        self.objetos = pygame.sprite.Group()
        self.objetos.add(Objeto(575, 500, 50, 150))
        self.objetos.add(Objeto(915, 590 , 300, 120))
        self.objetos.add(Objeto(650, 5, 150, 50))

        # Objeto de atração
        self.atracao = Sol(posicao=(self.largura // 2, self.altura // 2))

        self.menu = Menu()
        self.menu.mostrar = True
        
    def run(self):
        while self.running:
            if self.menu.mostrar_win:
                self.menu.draw(self.screen)
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.running = False
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        acao = self.menu.checar_clique(evento.pos)
                        if acao == 'sair':
                            self.running = False

            elif self.menu.mostrar:
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
                        # Verifica o clique para poder arrastar a bola
                        if np.linalg.norm(np.array(evento.pos) - self.bola.pos) <= self.bola.raio:
                            self.arrastando = True
                            self.bola.arrastando = True
                            self.pos_inicial = self.bola.pos.copy()
                    elif evento.type == pygame.MOUSEBUTTONUP:
                        # Verifica se soltou o clique para lançar a bola
                        if self.arrastando:
                            self.arrastando = False
                            self.bola.arrastando = False
                            destino = np.array(evento.pos, dtype=np.float64)
                            vetor_direcao = self.pos_inicial - destino
                            comprimento = np.linalg.norm(vetor_direcao)
                            # Verifica se a bola foi arrastada para longe o suficiente para ser lançada
                            if comprimento > 0:
                                vetor_direcao = vetor_direcao / comprimento
                                self.bola.velocidade = vetor_direcao * comprimento * self.controle_velocidade
                                self.bola.lancamento = True

                    elif evento.type == pygame.MOUSEMOTION and self.arrastando:
                        self.bola.pos = np.array(evento.pos, dtype=np.float64)

                # Atualizar a bola
                self.bola.update(self.largura, self.altura)

                # Aplicar força de atração do objeto na bola
                self.atracao.aplicar_forca(self.bola)

                # Verifica colisão com inimigos
                for inimigo in self.inimigos:
                    if pygame.sprite.collide_rect(self.bola, inimigo):
                        self.inimigos.remove(inimigo)
                        break

                if not self.inimigos:
                    self.menu.mostrar_win = True

                # Verifica colisão com objetos
                colisao_objeto = pygame.sprite.spritecollide(self.bola, self.objetos, False)
                if colisao_objeto and not self.arrastando:
                    self.bola.resetar()

                # Desenhar o fundo e os objetos
                self.screen.blit(self.fundo, (0, 0))
                self.atracao.draw(self.screen)
                self.bola.draw(self.screen)
                self.inimigos.draw(self.screen)
                self.objetos.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)

    pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    game = Game()
    game.run()
