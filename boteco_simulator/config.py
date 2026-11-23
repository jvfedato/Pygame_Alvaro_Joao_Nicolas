"""
config.py - Configurações do jogo

Aqui ficam todos os números e cores do jogo num lugar só,
pra não precisar ficar caçando nos outros arquivos.
Se quiser mudar alguma coisa (tamanho, atrito, cor), é só mudar aqui.
"""

# --- Janela ---
LARGURA_TELA = 1000
ALTURA_TELA = 600
FPS = 60                     # quantas vezes por segundo a tela atualiza
TITULO = "Boteco Simulator"

# --- Mesa ---
MARGEM_MESA = 60             # espaço entre a borda da janela e a mesa
LARGURA_BORDA = 30           # grossura da madeira em volta do pano
RAIO_CACAPA = 22

# --- Bolas ---
RAIO_BOLA = 11
ATRITO = 0.99                # a velocidade é multiplicada por isso a cada quadro
VELOCIDADE_MINIMA = 0.05     # mais lento que isso, a bola para
PERDA_TABELA = 0.8           # ao bater na tabela, a bola fica com 80% da velocidade
PASSOS_POR_QUADRO = 10       # cada quadro é dividido em 10 passinhos (a bola não atravessa outra)

# --- Taco ---
FORCA_MAXIMA = 18
VELOCIDADE_CARGA = 0.35      # quanto a força sobe por quadro segurando o mouse

# --- Cores (vermelho, verde, azul) ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE_PANO = (20, 110, 60)
MADEIRA = (110, 60, 25)
MADEIRA_ESCURA = (70, 35, 15)
FUNDO = (35, 25, 20)
AMARELO = (240, 200, 40)
VERMELHO = (200, 40, 40)
AZUL = (40, 80, 200)
LARANJA = (230, 120, 30)
ROXO = (120, 40, 150)
VERDE = (30, 150, 60)
MARROM = (120, 60, 30)

# Cor de cada bola pelo número dela
CORES_BOLAS = {
    1: AMARELO,
    2: AZUL,
    3: VERMELHO,
    4: ROXO,
    5: LARANJA,
    6: VERDE,
    7: MARROM,
    8: PRETO,
}

# Tamanhos das bolas, dimensoes da mesa e cores das bolas foram pegos baseados em IA
