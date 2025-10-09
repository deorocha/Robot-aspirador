# Configurações da tela
LARGURA_TELA = 352
ALTURA_TELA = 500
TAMANHO_CELULA = 50
LARGURA_LINHA = 2
DIMENSOES_GRID = (7, 7)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (128, 128, 128)
VERMELHO = (255, 0, 0)
AZUL = (0, 120, 255)
VERDE = (0, 255, 0)
CINZA_CLARO = (200, 200, 200)
CINZA_ESCURO = (100, 100, 100)

# Ambiente
grid_ambiente = [
    [1, 0, 0, 0, 0, 0, 0], # Linha 1
    [0, 0, 3, 0, 0, 0, 0], # Linha 2
    [0, 0, 0, 0, 0, 0, 0], # Linha 3
    [0, 0, 0, 2, 0, 3, 0], # Linha 4
    [0, 0, 0, 0, 3, 4, 0], # Linha 5
    [0, 0, 0, 0, 0, 0, 0], # Linha 6
    [0, 0, 0, 0, 0, 0, 3]  # Linha 7
]
# 0 - Vazio (nenhum objeto)
# 1 - Robot 1 (R1)
# 2 - Robot 2 (R2)
# 3 - Lixo
# 4 - Ouro

# Constantes do jogo
DELAY_MOVIMENTO = 20
DELAY_SOM = 10
