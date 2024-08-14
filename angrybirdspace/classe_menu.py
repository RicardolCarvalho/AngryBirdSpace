import pygame

class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.fonte = pygame.font.SysFont('arial', 40)
        self.botao_jogar = pygame.Rect(450, 300, 300, 60)
        self.botao_como_jogar = pygame.Rect(450, 400, 300, 60)
        self.botao_voltar = pygame.Rect(450, 500, 300, 60)
        self.mostrar_como_jogar = False

    def draw(self, tela):
        tela.fill((0, 0, 0))

        if self.mostrar_como_jogar:
            texto_como_jogar = self.fonte.render(
                'Para jogar puxe a bolinha com o cursor como se fosse um estilingue e acerte os pontos verde',True, (255, 255, 255))
            
            tela.blit(texto_como_jogar, (50, 200))

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
        return None
