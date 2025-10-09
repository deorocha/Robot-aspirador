import pygame
import sys
from config import *
from classes import Robo, Lixo, Ouro, Botao
from funcoes import *

# Inicialização
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Robôs de Limpeza")
relogio = pygame.time.Clock()

# Carregar recursos
som_movimento = carregar_som("./sounds/beep.mp3", 0.5)
som_vacuum = carregar_som("./sounds/vacuum.mp3", 0.5)
som_burning = carregar_som("./sounds/burning.mp3", 0.5)
som_vitoria = carregar_som("./sounds/victory.mp3", 0.7)  # Novo som de vitória

imagem_robo1 = carregar_imagem("./images/robot1.png", (TAMANHO_CELULA-10, TAMANHO_CELULA-6))
imagem_robo2 = carregar_imagem("./images/robot2.png", (TAMANHO_CELULA-10, TAMANHO_CELULA-6))
imagem_lixo = carregar_imagem("./images/lixo.png", (TAMANHO_CELULA-10, TAMANHO_CELULA-6))
imagem_ouro = carregar_imagem("./images/gold.png", (TAMANHO_CELULA-10, TAMANHO_CELULA-6))

# Inicializar ambiente
pos_r1, pos_r2, posicoes_lixo, pos_ouro = inicializar_ambiente()
robo_aspirador = Robo(AZUL, pos_r1, imagem_robo1)
robo_incinerador = Robo(VERMELHO, pos_r2, imagem_robo2)
lista_lixo = [Lixo(pos, imagem_lixo) for pos in posicoes_lixo]
ouro = Ouro(pos_ouro, imagem_ouro) if pos_ouro else None
botao_limpar = Botao(LARGURA_TELA//2 - 50, 380, 100, 30, "Limpar")

# Estado do jogo
estado_jogo = {
    'lixo_carregando': None,
    'pontuacao': 0,
    'mensagem_atual': "Pressione 'Limpar' para iniciar a limpeza automática",
    'modo_automatico': False,
    'ambiente_limpo': False,  # Novo estado para controlar se o ambiente está limpo
    'caminho_atual': [],
    'indice_caminho': 0,
    'aguardando': 0,
    'estado': "procurando",
    'som_movimento_tocado': False,
    'som_vacuum_tocando': False,
    'som_burning_tocando': False,
    'vacuum_channel': None,
    'burning_channel': None
}

# Loop principal
executando = True
while executando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            executando = False

    # Atualizar botão
    botao_limpar.atualizar(eventos)
    
    # Iniciar limpeza automática
    if botao_limpar.clicado and not estado_jogo['modo_automatico'] and (lista_lixo or (ouro and not ouro.coletado)):
        estado_jogo['modo_automatico'] = True
        estado_jogo['mensagem_atual'] = "Procurando Lixo..."
        estado_jogo['estado'] = "procurando"
        estado_jogo['som_movimento_tocado'] = False

    # Lógica do modo automático
    if estado_jogo['modo_automatico']:
        processar_modo_automatico(estado_jogo, robo_aspirador, robo_incinerador, 
                                 lista_lixo, ouro, som_movimento, som_vacuum, som_burning, som_vitoria)

    # Renderizar
    tela.fill(BRANCO)
    desenhar_grid(tela)
    
    # Desenhar ouro se não foi coletado
    if ouro and not ouro.coletado:
        ouro.desenhar(tela)
    
    # Desenhar lixo
    for item_lixo in lista_lixo:
        item_lixo.desenhar(tela)
    
    # Desenhar robôs
    robo_incinerador.desenhar(tela)
    robo_aspirador.desenhar(tela)
    
    # Desenhar botão
    botao_limpar.desenhar(tela)
    
    # UI
    fonte = pygame.font.SysFont(None, 24)
    fonte_mensagens = pygame.font.SysFont(None, 20)
    
    texto_pontuacao = fonte.render(f"Lixo Incinerado: {estado_jogo['pontuacao']}/{estado_jogo['pontuacao'] + len(lista_lixo)}", True, PRETO)
    tela.blit(texto_pontuacao, (10, 360))
    
    texto_mensagem = fonte_mensagens.render(estado_jogo['mensagem_atual'], True, PRETO)
    tela.blit(texto_mensagem, (10, 420))
    
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()
