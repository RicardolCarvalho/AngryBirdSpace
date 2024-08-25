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
        
        self.trajetoria = []  # Lista para armazenar a trajetória

    def calcular_trajetoria(self):
        self.trajetoria = []
        dt = 0.1  # Intervalo de tempo para calcular a trajetória
        t = 0
        while True:
            # Calcula a posição da bola no tempo t
            x = self.bola.inicial_pos[0] + self.bola.velocidade[0] * t
            y = self.bola.inicial_pos[1] + self.bola.velocidade[1] * t + 0.5 * self.bola.gravidade[1] * t ** 2

            # Adiciona a posição à trajetória
            self.trajetoria.append((x, y))

            # Verifica se a bola saiu da tela
            if x < 0 or x > self.largura or y > self.altura:
                break

            t += dt

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
                            # Recalcula a trajetória ao começar o arrasto
                            vetor_direcao = self.pos_inicial - np.array(evento.pos, dtype=np.float64)
                            comprimento = np.linalg.norm(vetor_direcao)
                            if comprimento > 0:
                                vetor_direcao = vetor_direcao / comprimento
                                self.bola.velocidade = vetor_direcao * comprimento * self.controle_velocidade
                                self.calcular_trajetoria()

                    elif evento.type == pygame.MOUSEBUTTONUP:
                        # Verifica se soltou o clique para lançar a bola
                        if self.arrastando:
                            self.arrastando = False
                            self.bola.arrastando = False
                            destino = np.array(evento.pos, dtype=np.float64)
                            vetor_direcao = self.pos_inicial - destino
                            comprimento = np.linalg.norm(vetor_direcao)
                            if comprimento > 0:
                                vetor_direcao = vetor_direcao / comprimento
                                self.bola.velocidade = vetor_direcao * comprimento * self.controle_velocidade
                                self.bola.lancamento = True
                                self.calcular_trajetoria()  # Recalcula a trajetória após o lançamento

                    elif evento.type == pygame.MOUSEMOTION and self.arrastando:
                        self.bola.pos = np.array(evento.pos, dtype=np.float64)
                        # Recalcula a trajetória enquanto arrasta
                        vetor_direcao = self.pos_inicial - self.bola.pos
                        comprimento = np.linalg.norm(vetor_direcao)
                        if comprimento > 0:
                            vetor_direcao = vetor_direcao / comprimento
                            self.bola.velocidade = vetor_direcao * comprimento * self.controle_velocidade
                            self.calcular_trajetoria()

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

                # Desenhar a trajetória
                if self.trajetoria and self.arrastando:
                    tamanho = len(self.trajetoria)
                    metade = (tamanho // 2) // 2
                    pygame.draw.lines(self.screen, (255, 255, 0), False, self.trajetoria[:metade], 2)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
