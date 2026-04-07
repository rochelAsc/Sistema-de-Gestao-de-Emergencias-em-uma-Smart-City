import pygame

# ==========================
# TELA
# ==========================
LARGURA = 700
ALTURA = 700

COLS = 30
ROWS = 30
TILE_SIZE = LARGURA // COLS

# ==========================
# TIPOS (LÓGICA)
# ==========================
VAZIO = 0
FOGO = 1
VITIMA = 2

# ==========================
# CAMINHOS
# ==========================
CAMINHO_CIDADE = "imgs/cidade_final.png"

PASTA_FOGO = "imgs/Fogo"
PASTA_VITIMA = "imgs/Vitima"

PASTA_DRONE = "imgs/drone"

PASTA_CARRO_D = "imgs/Carro_Bombeiro/Direita"
PASTA_CARRO_E = "imgs/Carro_Bombeiro/Esquerda"
PASTA_CARRO_C = "imgs/Carro_Bombeiro/Cima"
PASTA_CARRO_B = "imgs/Carro_Bombeiro/Baixo"

PASTA_BOMBEIRO = "imgs/Bombeiro"

SOCORRISTA1 = "imgs/Socorrista_1"
SOCORRISTA2 = "imgs/Socorrista_2"

# ==========================
# TAMANHOS
# ==========================
TAMANHO_DRONE = (40, 40)
TAMANHO_BOMBEIRO = (40, 40)
TAMANHO_SOCORRISTA = (40, 40)
TAMANHO_FOGO = (30, 30)
TAMANHO_VITIMA = (25, 25)