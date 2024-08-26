import pygame
import os
class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        caminho = os.path.join(os.path.dirname(__file__), 'img/fundo.png')
        self.image = pygame.image.load(caminho)
        self.fundo = pygame.transform.scale(self.image, (1200, 700))
        self.fonte = pygame.font.SysFont('arial', 40)
        self.fonte_menor = pygame.font.SysFont('arial', 30)
        self.botao_jogar = pygame.Rect(450, 300, 300, 60)
        self.botao_como_jogar = pygame.Rect(450, 400, 300, 60)
        self.botao_voltar = pygame.Rect(450, 500, 300, 60)
        self.botao_sair = pygame.Rect(450, 600, 300, 60)
        self.mostrar_como_jogar = False
        self.mostrar_win = False

    def draw(self, tela):
        tela.blit(self.fundo, (0,0))

        if self.mostrar_win:
            texto_win = self.fonte.render('Você venceu!', True, (255, 255, 255))
            tela.blit(texto_win, (450, 300))

            pygame.draw.rect(tela, (128, 0, 0), self.botao_sair)
            sair = self.fonte.render('Sair', True, (255, 255, 255))
            tela.blit(sair, (self.botao_sair.x + 90, self.botao_sair.y + 10))

        elif self.mostrar_como_jogar:
            # Texto sobre como jogar
            texto_como_jogar = self.fonte_menor.render('Para jogar puxe o alien com o cursor como se fosse', True, (255, 255, 255))
            texto_como_jogar2 = self.fonte_menor.render('um estilingue e acerte os robos', True, (255, 255, 255))
            texto_como_jogar3 = self.fonte_menor.render('Dica: utilize o sol para mudar a trajetoria do alien e sua velocidade', True, (255, 255, 255))
            tela.blit(texto_como_jogar, (50, 150))
            tela.blit(texto_como_jogar2, (50, 180))
            tela.blit(texto_como_jogar3, (50, 210))

            # Explicação matemática
            texto_matematica1 = self.fonte_menor.render('A trajetória da bola é influenciada por duas forças principais:', True, (255, 255, 255))
            texto_matematica2 = self.fonte_menor.render('1. Gravidade: Faz a bola acelerar para baixo a uma taxa constante.', True, (255, 255, 255))
            texto_matematica3 = self.fonte_menor.render('2. Atração: Uma força radial aplicada pela estrela ao centro.', True, (255, 255, 255))
            texto_matematica4 = self.fonte_menor.render('Essas forças são calculadas e somadas para determinar a', True, (255, 255, 255))
            texto_matematica5 = self.fonte_menor.render('velocidade e a nova posição da bola a cada quadro.', True, (255, 255, 255))
            tela.blit(texto_matematica1, (50, 260))
            tela.blit(texto_matematica2, (50, 290))
            tela.blit(texto_matematica3, (50, 320))
            tela.blit(texto_matematica4, (50, 350))
            tela.blit(texto_matematica5, (50, 380))

            pygame.draw.rect(tela, (128, 0, 0), self.botao_voltar)
            voltar = self.fonte.render('Voltar', True, (255, 255, 255))
            tela.blit(voltar, (self.botao_voltar.x + 90, self.botao_voltar.y + 10))

        else:
            pygame.draw.rect(tela, (0, 0, 0), self.botao_jogar)
            pygame.draw.rect(tela, (0, 0, 0), self.botao_como_jogar)

            jogar = self.fonte.render('Jogar', True, (255, 255, 255))
            como_jogar = self.fonte.render('Como Jogar', True, (255, 255, 255))

            tela.blit(jogar, (self.botao_jogar.x + 10, self.botao_jogar.y + 10))
            tela.blit(como_jogar, (self.botao_como_jogar.x + 10, self.botao_como_jogar.y + 10))

    def checar_clique(self, pos):
        if self.mostrar_como_jogar:
            if self.botao_voltar.collidepoint(pos):
                self.mostrar_como_jogar = False
        else:
            if self.botao_jogar.collidepoint(pos):
                return 'comecar'
            elif self.botao_como_jogar.collidepoint(pos):
                self.mostrar_como_jogar = True
            elif self.botao_sair.collidepoint(pos):
                return 'sair'
        return None
