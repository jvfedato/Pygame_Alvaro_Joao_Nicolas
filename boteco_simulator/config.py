"""
Configurações gerais do Boteco Simulator.

Aqui ficam as configuracoes sem precisar ficar cacando em outros arquivos. 
"""

# ---------------- Janela ----------------
LARGURA_TELA = 1000          # largura da janela em pixels
ALTURA_TELA = 600            # altura da janela em pixels
FPS = 60                     # quadros por segundo (quantas vezes a tela atualiza)
TITULO = "Boteco Simulator"

# ---------------- Mesa ----------------
MARGEM_MESA = 60             # distância da borda da janela até a madeira da mesa
LARGURA_BORDA = 30           # espessura da madeira (tabela) em volta do pano
RAIO_CACAPA = 22             # raio das caçapas (buracos)

# ---------------- Bolas ----------------
RAIO_BOLA = 11               # raio de cada bola em pixels
ATRITO = 0.985               # a cada quadro a velocidade é multiplicada por isso (perde 1,5%)
VELOCIDADE_MINIMA = 0.05     # abaixo disso consideramos a bola parada
PERDA_TABELA = 0.8           # ao bater na tabela a bola mantém 80% da velocidade

# ---------------- Taco ----------------
FORCA_MAXIMA = 18            # velocidade máxima que a tacada pode dar à bola branca
VELOCIDADE_CARGA = 0.35      # quanto a força aumenta por quadro segurando o mouse

# ---------------- Cores (R, G, B) ----------------
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

# Cor de cada bola numerada (índice = número da bola)
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
