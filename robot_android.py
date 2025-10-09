import pygame
import random
import sys
import time
import os

pygame.init()

# Configurações da tela
LARGURA_TELA = 1050
ALTURA_TELA = 1200 
TAMANHO_CELULA = 150
LARGURA_LINHA = 4
DIMENSOES_GRID = (7, 7)  # (colunas, linhas)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
VERMELHO = (255, 0, 0)
AZUL = (0, 120, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
CINZA_CLARO = (200, 200, 200)
CINZA_ESCURO = (100, 100, 100)

# Criação da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Robôs de Limpeza")
relogio = pygame.time.Clock()

# Define objetos do Ambiente - ADICIONADO OURO NA POSIÇÃO (5,6)
grid_ambiente = [
    [1, 0, 0, 0, 0, 0, 0],  # Linha 0
    [0, 0, 3, 0, 0, 0, 0],  # Linha 1
    [0, 0, 0, 0, 0, 0, 0],  # Linha 2
    [0, 0, 0, 2, 0, 3, 0],  # Linha 3
    [0, 0, 0, 0, 3, 0, 0],  # Linha 4
    [0, 0, 0, 0, 0, 0, 4],  # Linha 5 - OURO ADICIONADO AQUI
    [0, 0, 0, 0, 0, 0, 3]   # Linha 6
]
# 0 - Empty (nenhum objeto)
# 1 - Robot 1 (R1)
# 2 - Robot 2 (R2)
# 3 - Lixo
# 4 - Ouro (NOVO)

# --- Função Carregar sons ---
def carregar_som(nome_arquivo):
    """Carrega um arquivo de som"""
    try:
        som = pygame.mixer.Sound(nome_arquivo)
        return som
    except pygame.error:
        print(f"Erro ao carregar som: {nome_arquivo}")
        return None

# Carrega os sons - ADICIONADO SOM DE VITÓRIA
som_movimento = carregar_som("./sounds/beep.mp3")
som_vacuum = carregar_som("./sounds/vacuum.mp3")
som_burning = carregar_som("./sounds/burning.mp3")
som_vitoria = carregar_som("./sounds/victory.mp3")  # NOVO

# Ajusta o volume dos sons
if som_movimento:
    som_movimento.set_volume(0.5)
if som_vacuum:
    som_vacuum.set_volume(0.7)
if som_burning:
    som_burning.set_volume(0.6)
if som_vitoria:  # NOVO
    som_vitoria.set_volume(0.8)

# --- Carregar imagens ---
def carregar_imagem(nome_arquivo, tamanho=None):
    """Carrega uma imagem e opcionalmente redimensiona"""
    try:
        imagem = pygame.image.load(nome_arquivo)
        if tamanho:
            imagem = pygame.transform.scale(imagem, tamanho)
        return imagem
    except pygame.error:
        print(f"Erro ao carregar imagem: {nome_arquivo}")
        # Fallback: criar uma superfície colorida
        superficie = pygame.Surface((TAMANHO_CELULA,  TAMANHO_CELULA))
        if "robo1" in nome_arquivo:
            superficie.fill(AZUL)
        elif "robo2" in nome_arquivo:
            superficie.fill(VERMELHO)
        elif "ouro" in nome_arquivo or "gold" in nome_arquivo:  # NOVO
            superficie.fill(AMARELO)
        else:
            superficie.fill(VERDE)
        return superficie

# Carrega as imagens - ADICIONADO IMAGEM DO OURO
try:
    # Imagens para os robôs e lixo
    imagem_robo1 = carregar_imagem("./images/robot1.png", (TAMANHO_CELULA-10, TAMANHO_CELULA-10))
    imagem_robo2 = carregar_imagem("./images/robot2.png", (TAMANHO_CELULA-10, TAMANHO_CELULA-10))
    imagem_lixo = carregar_imagem("./images/lixo.png", (TAMANHO_CELULA-10, TAMANHO_CELULA-10))
    imagem_ouro = carregar_imagem("./images/gold.png", (TAMANHO_CELULA-10, TAMANHO_CELULA-10))  # NOVO
except:
    # Fallback de carregamento das imagens
    imagem_robo1 = None
    imagem_robo2 = None
    imagem_lixo = None
    imagem_ouro = None  # NOVO

# --- Definição das classes ---
class Robo:
    """Classe base para os robôs"""
    def __init__(self, cor, posicao_grid, imagem=None):
        self.cor = cor
        self.largura = TAMANHO_CELULA - 10  # Um pouco menor que a célula
        self.altura = TAMANHO_CELULA - 10
        self.posicao_grid = posicao_grid  # Posição (x, y) no grid
        self.imagem = imagem
        self.atualizar_rect()

    def atualizar_rect(self):
        """Atualiza o retângulo de colisão e desenho com base na posição do grid"""
        x = self.posicao_grid[0] * TAMANHO_CELULA + (TAMANHO_CELULA - self.largura) // 2 + LARGURA_LINHA
        y = self.posicao_grid[1] * TAMANHO_CELULA + (TAMANHO_CELULA - self.altura) // 2 + LARGURA_LINHA
        self.rect = pygame.Rect(x, y, self.largura, self.altura)

    def desenhar(self, superficie):
        """Desenha o robô na tela"""
        if self.imagem:
            # Centraliza a imagem na célula
            pos_x = self.rect.x + (self.rect.width - self.imagem.get_width()) // 2
            pos_y = self.rect.y + (self.rect.height - self.imagem.get_height()) // 2
            superficie.blit(self.imagem, (pos_x, pos_y))
        else:
            # Fallback para desenho geométrico se a imagem não carregar
            pygame.draw.rect(superficie, self.cor, self.rect, border_radius=10)
            pygame.draw.rect(superficie, PRETO, self.rect.inflate(-10, -10), border_radius=5, width=2)

class Lixo:
    """Classe para representar os itens de lixo"""
    def __init__(self, posicao_grid, imagem=None):
        self.posicao_grid = posicao_grid
        self.carregado = False
        self.raio = 8
        self.imagem = imagem
        self.atualizar_posicao_tela()

    def atualizar_posicao_tela(self):
        """Calcula a posição na tela com base no grid"""
        self.x = self.posicao_grid[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2 + LARGURA_LINHA
        self.y = self.posicao_grid[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2 + LARGURA_LINHA

    def desenhar(self, superficie):
        """Desenha o lixo como uma imagem ou círculo verde se não estiver carregado"""
        if not self.carregado:
            if self.imagem:
                # Centraliza a imagem na célula
                pos_x = self.x - self.imagem.get_width() // 2
                pos_y = self.y - self.imagem.get_height() // 2
                superficie.blit(self.imagem, (pos_x, pos_y))
            else:
                # Fallback para desenho geométrico se a imagem não carregar
                pygame.draw.circle(superficie, VERDE, (self.x, self.y), self.raio)

# NOVA CLASSE PARA O OURO
class Ouro:
    """Classe para representar a moeda de ouro"""
    def __init__(self, posicao_grid, imagem=None):
        self.posicao_grid = posicao_grid
        self.coletado = False
        self.raio = 12
        self.imagem = imagem
        self.atualizar_posicao_tela()

    def atualizar_posicao_tela(self):
        """Calcula a posição na tela com base no grid"""
        self.x = self.posicao_grid[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2 + LARGURA_LINHA
        self.y = self.posicao_grid[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2 + LARGURA_LINHA

    def desenhar(self, superficie):
        """Desenha o ouro como uma imagem ou círculo amarelo se não estiver coletado"""
        if not self.coletado:
            if self.imagem:
                # Centraliza a imagem na célula
                pos_x = self.x - self.imagem.get_width() // 2
                pos_y = self.y - self.imagem.get_height() // 2
                superficie.blit(self.imagem, (pos_x, pos_y))
            else:
                # Fallback para desenho geométrico se a imagem não carregar
                pygame.draw.circle(superficie, AMARELO, (self.x, self.y), self.raio)

class Botao:
    """Classe para representar um botão"""
    def __init__(self, x, y, largura, altura, texto, cor_normal=CINZA_CLARO, cor_hover=CINZA_ESCURO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_atual = cor_normal
        self.fonte = pygame.font.SysFont(None, 60)
        self.clicado = False
        
    def desenhar(self, superficie):
        """Desenha o botão na tela"""
        pygame.draw.rect(superficie, self.cor_atual, self.rect, border_radius=5)
        pygame.draw.rect(superficie, PRETO, self.rect, 2, border_radius=5)
        
        texto_surface = self.fonte.render(self.texto, True, PRETO)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        superficie.blit(texto_surface, texto_rect)
        
    def atualizar(self, eventos):
        """Atualiza o estado do botão com base nos eventos"""
        mouse_pos = pygame.mouse.get_pos()
        self.clicado = False
        
        # Verifica se o mouse está sobre o botão
        if self.rect.collidepoint(mouse_pos):
            self.cor_atual = self.cor_hover
            # Verifica se o botão foi clicado
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.clicado = True
        else:
            self.cor_atual = self.cor_normal

# --- Funções de apoio ---
def desenhar_grid(superficie):
    """Desenha as linhas do grid na tela"""
    # Desenha linhas horizontais
    mt = 150
    for linha in range(DIMENSOES_GRID[1] + 1):
        y = linha * TAMANHO_CELULA
        pygame.draw.line(superficie, CINZA, (0, y), (LARGURA_TELA, y), LARGURA_LINHA)
    # Desenha linhas verticais
    for coluna in range(DIMENSOES_GRID[0] + 1):
        x = coluna * TAMANHO_CELULA
        pygame.draw.line(superficie, CINZA, (x, 0), (x, LARGURA_TELA), LARGURA_LINHA)

def encontrar_caminho(pos_atual, pos_destino):
    """Encontra um caminho simples entre duas posições no grid"""
    caminho = []
    x_atual, y_atual = pos_atual
    x_dest, y_dest = pos_destino
    
    # Move horizontalmente primeiro, depois verticalmente
    while x_atual != x_dest:
        if x_atual < x_dest:
            x_atual += 1
        else:
            x_atual -= 1
        caminho.append((x_atual, y_atual))
    
    while y_atual != y_dest:
        if y_atual < y_dest:
            y_atual += 1
        else:
            y_atual -= 1
        caminho.append((x_atual, y_atual))
    
    return caminho

def inicializar_ambiente():
    """Inicializa o ambiente a partir da matriz fornecida"""
    pos_r1 = None
    pos_r2 = None
    posicoes_lixo = []
    pos_ouro = None  # NOVO
    
    # Percorre a matriz para encontrar as posições
    for linha in range(len(grid_ambiente)):
        for coluna in range(len(grid_ambiente[linha])):
            valor = grid_ambiente[linha][coluna]
            if valor == 1:  # R1
                pos_r1 = (coluna, linha)
            elif valor == 2:  # R2
                pos_r2 = (coluna, linha)
            elif valor == 3:  # Lixo
                posicoes_lixo.append((coluna, linha))
            elif valor == 4:  # Ouro (NOVO)
                pos_ouro = (coluna, linha)
    
    return pos_r1, pos_r2, posicoes_lixo, pos_ouro  # MODIFICADO

# --- Inicialização  ---
# Inicializa o ambiente a partir da matriz
pos_r1, pos_r2, posicoes_lixo, pos_ouro = inicializar_ambiente()  # MODIFICADO

# Cria os robôs com as posições da matriz
robo_aspirador = Robo(AZUL, pos_r1, imagem_robo1)
robo_incinerador = Robo(VERMELHO, pos_r2, imagem_robo2)

# Cria a lista de lixo a partir das posições da matriz
lista_lixo = [Lixo(pos, imagem_lixo) for pos in posicoes_lixo]

# NOVO: Cria o objeto ouro
ouro = Ouro(pos_ouro, imagem_ouro) if pos_ouro else None

# Cria o botão
botao_limpar = Botao(800 , 1080, 250, 80, "Limpar")

# Variáveis de controle - ADICIONADAS NOVAS VARIÁVEIS
lixo_carregando = None
pontuacao = 0
fonte = pygame.font.SysFont(None, 80)
fonte_mensagens = pygame.font.SysFont(None, 60)
mensagem_atual = "Pressione 'Limpar' para iniciar a limpeza automática"
modo_automatico = False
caminho_atual = []
indice_caminho = 0
aguardando = 0
estado = "procurando"  # Estados: procurando, indo_para_lixo, pegando_lixo, indo_para_incinerador, incinerando, procurando_ouro, indo_para_ouro, coletando_ouro
ambiente_limpo = False  # NOVO: controla se o ambiente está limpo
delay_movimento = 10  # Delay entre movimentos (em frames)

# Variável para controlar se o som
som_movimento_tocado = False

# Variáveis de controle de som
som_vacuum_tocando = False
som_burning_tocando = False
vacuum_channel = None
burning_channel = None

# --- Loop principal ---
executando = True

while executando:
    eventos = pygame.event.get()
    
    # --- Tratamento de eventos ---
    for evento in eventos:
        if evento.type == pygame.QUIT:
            executando = False
    
    # Atualiza o botão
    botao_limpar.atualizar(eventos)
    
    # Inicia a limpeza automática quando o botão é pressionado
    if botao_limpar.clicado and not modo_automatico and (len(lista_lixo) > 0 or (ouro and not ouro.coletado)):
        modo_automatico = True
        mensagem_atual = "Procurando lixo..."
        estado = "procurando"
        som_movimento_tocado = False  # Resetar ao iniciar novo ciclo
        ambiente_limpo = False  # NOVO: resetar estado de limpeza
    
    # --- Lógica do modo automático ---
    if modo_automatico:
        if aguardando > 0:
            aguardando -= 1
        else:
            # FASE 1: LIMPEZA DO AMBIENTE
            if not ambiente_limpo:
                if estado == "procurando":
                    # Procura pelo lixo mais próximo
                    if lista_lixo:
                        # Encontra o lixo mais próximo
                        lixo_mais_proximo = min(lista_lixo, 
                                               key=lambda l: abs(l.posicao_grid[0] - robo_aspirador.posicao_grid[0]) + 
                                                             abs(l.posicao_grid[1] - robo_aspirador.posicao_grid[1]))
                        
                        # Calcula o caminho até o lixo
                        caminho_atual = encontrar_caminho(robo_aspirador.posicao_grid, lixo_mais_proximo.posicao_grid)
                        indice_caminho = 0
                        estado = "indo_para_lixo"
                        mensagem_atual = "Lixo encontrado! Indo coletar..."
                        som_movimento_tocado = False  # Resetar para o novo movimento
                    else:
                        ambiente_limpo = True  # NOVO: ambiente está limpo
                        estado = "procurando_ouro"  # NOVO: passar para busca do ouro
                        mensagem_atual = "Ambiente limpo! Procurando ouro..."
                
                elif estado == "indo_para_lixo":
                    if indice_caminho < len(caminho_atual):
                        # Se o som ainda não foi tocado para este movimento, toca o som
                        if not som_movimento_tocado and som_movimento:
                            som_movimento.play()
                            som_movimento_tocado = True
                            # Aguarda um pouco para o som ser ouvido antes do movimento
                            aguardando = 10  # Pequeno delay para o som
                        else:
                            # Move para a próxima célula após o som
                            robo_aspirador.posicao_grid = caminho_atual[indice_caminho]
                            robo_aspirador.atualizar_rect()
                            indice_caminho += 1
                            
                            # Aguarda antes do próximo movimento
                            aguardando = delay_movimento
                            som_movimento_tocado = False  # Resetar para o próximo movimento
                            
                            # Verifica se chegou ao lixo
                            if robo_aspirador.posicao_grid == caminho_atual[-1]:
                                estado = "pegando_lixo"
                                mensagem_atual = "Aspirando lixo..."
                                
                                # Inicia o som do vacuum
                                if som_vacuum and not som_vacuum_tocando:
                                    vacuum_channel = som_vacuum.play()
                                    som_vacuum_tocando = True
                    
                elif estado == "pegando_lixo":
                    # Verifica se o som do vacuum ainda está tocando
                    if som_vacuum_tocando and vacuum_channel.get_busy():
                        # Continua esperando o som terminar
                        pass
                    else:
                        # Som do vacuum terminou, pega o lixo
                        som_vacuum_tocando = False
                        for item_lixo in lista_lixo:
                            if item_lixo.posicao_grid == robo_aspirador.posicao_grid and not item_lixo.carregado:
                                item_lixo.carregado = True
                                lixo_carregando = item_lixo
                                break
                        
                        # Calcula o caminho até o incinerador
                        caminho_atual = encontrar_caminho(robo_aspirador.posicao_grid, robo_incinerador.posicao_grid)
                        indice_caminho = 0
                        estado = "indo_para_incinerador"
                        mensagem_atual = "Levando lixo ao incinerador..."
                        som_movimento_tocado = False  # Resetar para o novo movimento
                
                elif estado == "indo_para_incinerador":
                    if indice_caminho < len(caminho_atual):
                        # Se o som ainda não foi tocado para este movimento, toca o som
                        if not som_movimento_tocado and som_movimento:
                            som_movimento.play()
                            som_movimento_tocado = True
                            # Aguarda um pouco para o som ser ouvido antes do movimento
                            aguardando = 10  # Pequeno delay para o som
                        else:
                            # Move para a próxima célula após o som
                            robo_aspirador.posicao_grid = caminho_atual[indice_caminho]
                            robo_aspirador.atualizar_rect()
                            indice_caminho += 1
                            
                            # Aguarda antes do próximo movimento
                            aguardando = delay_movimento
                            som_movimento_tocado = False  # Resetar para o próximo movimento
                            
                            # Atualiza a posição do lixo carregado
                            if lixo_carregando is not None:
                                lixo_carregando.posicao_grid = robo_aspirador.posicao_grid
                                lixo_carregando.atualizar_posicao_tela()
                            
                            # Verifica se chegou ao incinerador
                            if robo_aspirador.posicao_grid == caminho_atual[-1]:
                                estado = "incinerando"
                                mensagem_atual = "Incinerando lixo..."
                                
                                # Inicia o som do burning
                                if som_burning and not som_burning_tocando:
                                    burning_channel = som_burning.play()
                                    som_burning_tocando = True
                    
                elif estado == "incinerando":
                    # Verifica se o som do burning ainda está tocando
                    if som_burning_tocando and burning_channel.get_busy():
                        # Continua esperando o som terminar
                        pass
                    else:
                        # Som do burning terminou, incinera o lixo
                        som_burning_tocando = False
                        if lixo_carregando is not None:
                            lista_lixo.remove(lixo_carregando)
                            lixo_carregando = None
                            pontuacao += 1
                        
                        estado = "procurando"
                        mensagem_atual = "Lixo incinerado! Procurando mais lixo..."
            
            # FASE 2: BUSCA PELO OURO (APÓS AMBIENTE LIMPO) - NOVO
            else:
                if estado == "procurando_ouro":
                    if ouro and not ouro.coletado:
                        # Calcula o caminho até o ouro
                        caminho_atual = encontrar_caminho(robo_aspirador.posicao_grid, ouro.posicao_grid)
                        indice_caminho = 0
                        estado = "indo_para_ouro"
                        mensagem_atual = "Ouro encontrado! Indo coletar..."
                        som_movimento_tocado = False
                    else:
                        modo_automatico = False
                        mensagem_atual = "Jogo Concluído!"
                
                elif estado == "indo_para_ouro":
                    if indice_caminho < len(caminho_atual):
                        # Se o som ainda não foi tocado para este movimento, toca o som
                        if not som_movimento_tocado and som_movimento:
                            som_movimento.play()
                            som_movimento_tocado = True
                            # Aguarda um pouco para o som ser ouvido antes do movimento
                            aguardando = 10  # Pequeno delay para o som
                        else:
                            # Move para a próxima célula após o som
                            robo_aspirador.posicao_grid = caminho_atual[indice_caminho]
                            robo_aspirador.atualizar_rect()
                            indice_caminho += 1
                            
                            # Aguarda antes do próximo movimento
                            aguardando = delay_movimento
                            som_movimento_tocado = False  # Resetar para o próximo movimento
                            
                            # Verifica se chegou ao ouro
                            if robo_aspirador.posicao_grid == caminho_atual[-1]:
                                estado = "coletando_ouro"
                                mensagem_atual = "Coletando ouro..."
                
                elif estado == "coletando_ouro":
                    if ouro and not ouro.coletado:
                        ouro.coletado = True
                        if som_vitoria:
                            som_vitoria.play()
                        mensagem_atual = "Jogo Ganho! Parabéns!"
                        modo_automatico = False
    
    # --- Verifica condição de vitória ---
    if len(lista_lixo) == 0 and modo_automatico and not ambiente_limpo:
        ambiente_limpo = True
        estado = "procurando_ouro"
        mensagem_atual = "Ambiente totalmente limpo! Procurando ouro..."

    # --- Desenho na tela ---
    tela.fill(BRANCO)
    desenhar_grid(tela)
    
    # Desenha o ouro se não foi coletado - NOVO
    if ouro and not ouro.coletado:
        ouro.desenhar(tela)
    
    # Desenha o lixo
    for item_lixo in lista_lixo:
        item_lixo.desenhar(tela)
    
    # Desenha os robôs
    robo_incinerador.desenhar(tela)
    robo_aspirador.desenhar(tela)
    
    # Desenha o botão
    botao_limpar.desenhar(tela)
    
    # Desenha a pontuação
    texto_pontuacao = fonte.render(f"Lixo Incinerado: {pontuacao}/{pontuacao + len(lista_lixo)}", True, PRETO)
    tela.blit(texto_pontuacao, (10, 1100))
    
    # Desenha a mensagem atual
    texto_mensagem = fonte_mensagens.render(mensagem_atual, True, PRETO)
    tela.blit(texto_mensagem, (10, 1200))
    
    pygame.display.flip()
    relogio.tick(60)  # 60 FPS

pygame.quit()
sys.exit()
