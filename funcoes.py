import pygame
from config import *

def carregar_som(nome_arquivo, volume=1.0):
    try:
        som = pygame.mixer.Sound(nome_arquivo)
        som.set_volume(volume)
        return som
    except pygame.error:
        print(f"Erro ao carregar som: {nome_arquivo}")
        return None

def carregar_imagem(nome_arquivo, tamanho=None):
    try:
        imagem = pygame.image.load(nome_arquivo)
        if tamanho:
            imagem = pygame.transform.scale(imagem, tamanho)
        return imagem
    except pygame.error:
        print(f"Erro ao carregar imagem: {nome_arquivo}")
        superficie = pygame.Surface((TAMANHO_CELULA-10, TAMANHO_CELULA-10))
        if "robo1" in nome_arquivo:
            superficie.fill(AZUL)
        elif "robo2" in nome_arquivo:
            superficie.fill(VERMELHO)
        elif "ouro" in nome_arquivo or "gold" in nome_arquivo:
            superficie.fill(AMARELO)
        else:
            superficie.fill(VERDE)
        return superficie

def desenhar_grid(superficie):
    for linha in range(DIMENSOES_GRID[1] + 1):
        y = linha * TAMANHO_CELULA
        pygame.draw.line(superficie, CINZA, (0, y), (LARGURA_TELA, y), LARGURA_LINHA)
    for coluna in range(DIMENSOES_GRID[0] + 1):
        x = coluna * TAMANHO_CELULA
        pygame.draw.line(superficie, CINZA, (x, 0), (x, LARGURA_TELA), LARGURA_LINHA)

def encontrar_caminho(pos_atual, pos_destino):
    caminho = []
    x_atual, y_atual = pos_atual
    x_dest, y_dest = pos_destino
    
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
    pos_r1 = pos_r2 = None
    posicoes_lixo = []
    pos_ouro = None
    
    for linha in range(len(grid_ambiente)):
        for coluna in range(len(grid_ambiente[linha])):
            valor = grid_ambiente[linha][coluna]
            if valor == 1:
                pos_r1 = (coluna, linha)
            elif valor == 2:
                pos_r2 = (coluna, linha)
            elif valor == 3:
                posicoes_lixo.append((coluna, linha))
            elif valor == 4:
                pos_ouro = (coluna, linha)
    
    return pos_r1, pos_r2, posicoes_lixo, pos_ouro

def processar_modo_automatico(estado, robo_aspirador, robo_incinerador, lista_lixo, ouro, som_movimento, som_vacuum, som_burning, som_vitoria):
    if estado['aguardando'] > 0:
        estado['aguardando'] -= 1
        return

    # Fase 1: Limpeza do ambiente
    if not estado['ambiente_limpo']:
        if estado['estado'] == "procurando":
            if lista_lixo:
                lixo_mais_proximo = min(lista_lixo, 
                                       key=lambda l: abs(l.posicao_grid[0] - robo_aspirador.posicao_grid[0]) + 
                                                     abs(l.posicao_grid[1] - robo_aspirador.posicao_grid[1]))
                
                estado['caminho_atual'] = encontrar_caminho(robo_aspirador.posicao_grid, lixo_mais_proximo.posicao_grid)
                estado['indice_caminho'] = 0
                estado['estado'] = "indo_para_lixo"
                estado['mensagem_atual'] = "Lixo encontrado! Indo coletar..."
                estado['som_movimento_tocado'] = False
            else:
                estado['ambiente_limpo'] = True
                estado['estado'] = "procurando_ouro"
                estado['mensagem_atual'] = "Ambiente Limpo! Procurando ouro..."

        elif estado['estado'] == "indo_para_lixo":
            processar_movimento(estado, robo_aspirador, som_movimento, "pegando_lixo", "Aspirando o Lixo...")
            if estado['estado'] == "pegando_lixo" and som_vacuum and not estado['som_vacuum_tocando']:
                estado['vacuum_channel'] = som_vacuum.play()
                estado['som_vacuum_tocando'] = True

        elif estado['estado'] == "pegando_lixo":
            if estado['som_vacuum_tocando'] and estado['vacuum_channel'].get_busy():
                return
                
            estado['som_vacuum_tocando'] = False
            for item_lixo in lista_lixo:
                if item_lixo.posicao_grid == robo_aspirador.posicao_grid and not item_lixo.carregado:
                    item_lixo.carregado = True
                    estado['lixo_carregando'] = item_lixo
                    break
            
            estado['caminho_atual'] = encontrar_caminho(robo_aspirador.posicao_grid, robo_incinerador.posicao_grid)
            estado['indice_caminho'] = 0
            estado['estado'] = "indo_para_incinerador"
            estado['mensagem_atual'] = "Levando Lixo ao Incinerador..."
            estado['som_movimento_tocado'] = False

        elif estado['estado'] == "indo_para_incinerador":
            processar_movimento(estado, robo_aspirador, som_movimento, "incinerando", "Incinerando o Lixo...")
            
            if estado['lixo_carregando'] is not None:
                estado['lixo_carregando'].posicao_grid = robo_aspirador.posicao_grid
                estado['lixo_carregando'].atualizar_posicao_tela()
                
            if estado['estado'] == "incinerando" and som_burning and not estado['som_burning_tocando']:
                estado['burning_channel'] = som_burning.play()
                estado['som_burning_tocando'] = True

        elif estado['estado'] == "incinerando":
            if estado['som_burning_tocando'] and estado['burning_channel'].get_busy():
                return
                
            estado['som_burning_tocando'] = False
            if estado['lixo_carregando'] is not None:
                lista_lixo.remove(estado['lixo_carregando'])
                estado['lixo_carregando'] = None
                estado['pontuacao'] += 1
            
            estado['estado'] = "procurando"
            estado['mensagem_atual'] = "Lixo incinerado! Procurando mais Lixo..."
    
    # Fase 2: Busca pelo ouro (após ambiente limpo)
    else:
        if estado['estado'] == "procurando_ouro":
            if ouro and not ouro.coletado:
                estado['caminho_atual'] = encontrar_caminho(robo_aspirador.posicao_grid, ouro.posicao_grid)
                estado['indice_caminho'] = 0
                estado['estado'] = "indo_para_ouro"
                estado['mensagem_atual'] = "Ouro encontrado! Indo coletar..."
                estado['som_movimento_tocado'] = False
            else:
                estado['modo_automatico'] = False
                estado['mensagem_atual'] = "Jogo Concluído!"

        elif estado['estado'] == "indo_para_ouro":
            processar_movimento(estado, robo_aspirador, som_movimento, "coletando_ouro", "Coletando ouro...")
            
        elif estado['estado'] == "coletando_ouro":
            if ouro and not ouro.coletado:
                ouro.coletado = True
                if som_vitoria:
                    som_vitoria.play()
                estado['mensagem_atual'] = "Jogo Ganho! Parabéns!"
                estado['modo_automatico'] = False

def processar_movimento(estado, robo, som_movimento, proximo_estado, mensagem_proximo_estado):
    if estado['indice_caminho'] >= len(estado['caminho_atual']):
        return
        
    if not estado['som_movimento_tocado'] and som_movimento:
        som_movimento.play()
        estado['som_movimento_tocado'] = True
        estado['aguardando'] = DELAY_SOM
    else:
        robo.posicao_grid = estado['caminho_atual'][estado['indice_caminho']]
        robo.atualizar_rect()
        estado['indice_caminho'] += 1
        estado['aguardando'] = DELAY_MOVIMENTO
        estado['som_movimento_tocado'] = False
        
        if robo.posicao_grid == estado['caminho_atual'][-1]:
            estado['estado'] = proximo_estado
            estado['mensagem_atual'] = mensagem_proximo_estado
