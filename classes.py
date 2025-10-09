import pygame
from config import *

class Robo:
    def __init__(self, cor, posicao_grid, imagem=None):
        self.cor = cor
        self.largura = TAMANHO_CELULA - 10
        self.altura = TAMANHO_CELULA - 10
        self.posicao_grid = posicao_grid
        self.imagem = imagem
        self.atualizar_rect()

    def atualizar_rect(self):
        x = self.posicao_grid[0] * TAMANHO_CELULA + (TAMANHO_CELULA - self.largura) // 2 + LARGURA_LINHA
        y = self.posicao_grid[1] * TAMANHO_CELULA + (TAMANHO_CELULA - self.altura) // 2 + LARGURA_LINHA
        self.rect = pygame.Rect(x, y, self.largura, self.altura)

    def desenhar(self, superficie):
        if self.imagem:
            pos_x = self.rect.x + (self.rect.width - self.imagem.get_width()) // 2
            pos_y = self.rect.y + (self.rect.height - self.imagem.get_height()) // 2
            superficie.blit(self.imagem, (pos_x, pos_y))
        else:
            pygame.draw.rect(superficie, self.cor, self.rect, border_radius=10)
            pygame.draw.rect(superficie, PRETO, self.rect.inflate(-10, -10), border_radius=5, width=2)

class Lixo:
    def __init__(self, posicao_grid, imagem=None):
        self.posicao_grid = posicao_grid
        self.carregado = False
        self.imagem = imagem
        self.atualizar_posicao_tela()

    def atualizar_posicao_tela(self):
        self.x = self.posicao_grid[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2 + LARGURA_LINHA
        self.y = self.posicao_grid[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2 + LARGURA_LINHA

    def desenhar(self, superficie):
        if not self.carregado:
            if self.imagem:
                pos_x = self.x - self.imagem.get_width() // 2
                pos_y = self.y - self.imagem.get_height() // 2
                superficie.blit(self.imagem, (pos_x, pos_y))
            else:
                pygame.draw.circle(superficie, VERDE, (self.x, self.y), 8)

class Ouro:
    def __init__(self, posicao_grid, imagem=None):
        self.posicao_grid = posicao_grid
        self.coletado = False
        self.imagem = imagem
        self.atualizar_posicao_tela()

    def atualizar_posicao_tela(self):
        self.x = self.posicao_grid[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2 + LARGURA_LINHA
        self.y = self.posicao_grid[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2 + LARGURA_LINHA

    def desenhar(self, superficie):
        if not self.coletado:
            if self.imagem:
                pos_x = self.x - self.imagem.get_width() // 2
                pos_y = self.y - self.imagem.get_height() // 2
                superficie.blit(self.imagem, (pos_x, pos_y))
            else:
                pygame.draw.circle(superficie, AMARELO, (self.x, self.y), 10)

class Botao:
    def __init__(self, x, y, largura, altura, texto):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = CINZA_CLARO
        self.cor_hover = CINZA_ESCURO
        self.cor_atual = self.cor_normal
        self.fonte = pygame.font.SysFont(None, 28)
        self.clicado = False
        
    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor_atual, self.rect, border_radius=5)
        pygame.draw.rect(superficie, PRETO, self.rect, 2, border_radius=5)
        texto_surface = self.fonte.render(self.texto, True, PRETO)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        superficie.blit(texto_surface, texto_rect)
        
    def atualizar(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        self.clicado = False
        
        if self.rect.collidepoint(mouse_pos):
            self.cor_atual = self.cor_hover
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.clicado = True
        else:
            self.cor_atual = self.cor_normal
