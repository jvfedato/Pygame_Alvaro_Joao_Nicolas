"""
telas.py - As telas que não são a mesa

Menu, instruções, loja e fim de jogo. Aqui só DESENHA as telas e os botões.
Quem decide qual tela aparece é o main.py.
No começo tem as funções que desenham as bebidas do balcão do menu.
"""

import pygame
from config import LARGURA_TELA, FUNDO, BRANCO, AMARELO, MADEIRA, VERDE_PANO, CORES_BOLAS

MEIO_X = LARGURA_TELA // 2   # o x do meio da tela
ALTURA_BALCAO = 490          # altura do balcão onde ficam as bebidas

# Cores das bebidas
VIDRO_MARROM = (90, 45, 15)
CERVEJA = (235, 170, 30)
ESPUMA = (250, 245, 230)
WHISKY = (180, 95, 20)
ROLHA = (60, 30, 10)
GELO = (210, 235, 255)
CINZA_VIDRO = (200, 200, 200)
DOURADO = (200, 170, 60)


# --- Bebidas do balcão ---
# Todas recebem o x do meio do objeto e a "base" (o y onde ele encosta no balcão).
# As medidas são contadas da base pra cima: base - 75 é 75 pixels acima do balcão.

def desenhar_cerveja(tela, x, base):
    """Garrafa de cerveja marrom com rótulo."""
    pygame.draw.rect(tela, VIDRO_MARROM, (x - 13, base - 75, 26, 75), border_radius=6)   # corpo
    ombro = [(x - 13, base - 72), (x + 13, base - 72), (x + 5, base - 95), (x - 5, base - 95)]
    pygame.draw.polygon(tela, VIDRO_MARROM, ombro)                                        # ombro
    pygame.draw.rect(tela, VIDRO_MARROM, (x - 5, base - 120, 10, 26))                     # gargalo
    pygame.draw.rect(tela, DOURADO, (x - 6, base - 125, 12, 6), border_radius=2)          # tampinha
    pygame.draw.rect(tela, (235, 220, 170), (x - 13, base - 55, 26, 28))                  # rótulo
    pygame.draw.rect(tela, (180, 30, 30), (x - 13, base - 45, 26, 6))                     # faixa vermelha
    pygame.draw.line(tela, (150, 100, 60), (x - 8, base - 70), (x - 8, base - 60), 2)     # brilho


def desenhar_copo_americano(tela, x, base):
    """Copo americano com cerveja e espuma."""
    copo = [(x - 15, base - 45), (x + 15, base - 45), (x + 12, base), (x - 12, base)]
    pygame.draw.polygon(tela, CERVEJA, copo)                                              # cerveja
    pygame.draw.rect(tela, ESPUMA, (x - 15, base - 50, 30, 10), border_radius=4)          # espuma
    pygame.draw.polygon(tela, CINZA_VIDRO, copo, 2)                                       # vidro


def desenhar_whisky(tela, x, base):
    """Garrafa quadrada de whisky com rótulo preto."""
    pygame.draw.rect(tela, WHISKY, (x - 20, base - 80, 40, 80), border_radius=4)          # corpo
    pygame.draw.rect(tela, WHISKY, (x - 12, base - 92, 24, 14), border_radius=4)          # ombro
    pygame.draw.rect(tela, WHISKY, (x - 6, base - 110, 12, 20))                           # gargalo
    pygame.draw.rect(tela, ROLHA, (x - 7, base - 119, 14, 10), border_radius=2)           # rolha
    pygame.draw.rect(tela, (20, 20, 20), (x - 16, base - 62, 32, 32))                     # rótulo
    pygame.draw.rect(tela, DOURADO, (x - 16, base - 62, 32, 32), 2)                       # borda do rótulo
    pygame.draw.line(tela, DOURADO, (x - 10, base - 50), (x + 10, base - 50), 2)          # "letras"
    pygame.draw.line(tela, DOURADO, (x - 7, base - 42), (x + 7, base - 42), 2)


def desenhar_copo_whisky(tela, x, base):
    """Copo baixo com whisky e duas pedras de gelo."""
    pygame.draw.rect(tela, WHISKY, (x - 15, base - 18, 30, 17))                           # whisky
    pygame.draw.rect(tela, GELO, (x - 11, base - 24, 10, 10), border_radius=2)            # gelo 1
    pygame.draw.rect(tela, GELO, (x + 1, base - 21, 10, 10), border_radius=2)             # gelo 2
    pygame.draw.rect(tela, CINZA_VIDRO, (x - 17, base - 34, 34, 34), 2, border_radius=3)  # vidro


class Botao:
    """Um botão com texto que fica mais claro quando o mouse passa em cima."""

    def __init__(self, texto, x, y, largura=260, altura=55):
        """x e y são o CENTRO do botão."""
        self.texto = texto
        self.rect = pygame.Rect(0, 0, largura, altura)
        self.rect.center = (x, y)

    def desenhar(self, tela, fonte):
        """Desenha o botão (mais claro se o mouse estiver em cima)."""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            cor = (160, 95, 45)      # madeira clara
        else:
            cor = MADEIRA
        pygame.draw.rect(tela, cor, self.rect, border_radius=10)
        pygame.draw.rect(tela, AMARELO, self.rect, 3, border_radius=10)   # borda

        texto = fonte.render(self.texto, True, BRANCO)
        tela.blit(texto, texto.get_rect(center=self.rect.center))

    def foi_clicado(self, evento):
        """Diz se esse evento foi um clique esquerdo em cima do botão."""
        return (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                and self.rect.collidepoint(evento.pos))


class Telas:
    """Desenha o menu, as instruções, a loja e o fim."""

    def __init__(self):
        """Cria as fontes e os botões."""
        self.fonte_titulo = pygame.font.SysFont("arial", 64, bold=True)
        self.fonte_media = pygame.font.SysFont("arial", 28, bold=True)
        self.fonte = pygame.font.SysFont("arial", 20)

        # Botões do menu, um embaixo do outro (de 60 em 60 pixels)
        self.botao_jogar = Botao("Jogar", MEIO_X, 270, altura=50)
        self.botao_loja = Botao("Loja", MEIO_X, 330, altura=50)
        self.botao_instrucoes = Botao("Instruções", MEIO_X, 390, altura=50)
        self.botao_sair = Botao("Sair", MEIO_X, 450, altura=50)

        # Usado nas telas de instruções, loja e fim
        self.botao_voltar = Botao("Voltar ao menu", MEIO_X, 540)

        # Um botão pra cada melhoria da loja (o texto muda na hora de desenhar)
        self.botoes_loja = [
            Botao("", MEIO_X, 200, largura=480),
            Botao("", MEIO_X, 300, largura=480),
            Botao("", MEIO_X, 400, largura=480),
        ]

    def escrever(self, tela, texto, fonte, cor, y):
        """Escreve um texto centralizado na altura y."""
        imagem = fonte.render(texto, True, cor)
        tela.blit(imagem, imagem.get_rect(center=(MEIO_X, y)))

    def desenhar_menu(self, tela, moedas):
        """Tela inicial com título, bolas, balcão e botões."""
        tela.fill(FUNDO)

        # Faixa verde com as 8 bolas
        pygame.draw.rect(tela, VERDE_PANO, (0, 170, LARGURA_TELA, 60))
        for numero in range(1, 9):
            x = MEIO_X - 245 + numero * 55
            pygame.draw.circle(tela, CORES_BOLAS[numero], (x, 200), 18)
            pygame.draw.circle(tela, BRANCO, (x, 200), 8)

        # Balcão com as bebidas
        pygame.draw.rect(tela, MADEIRA, (0, ALTURA_BALCAO, LARGURA_TELA, 16))
        desenhar_cerveja(tela, 110, ALTURA_BALCAO)
        desenhar_cerveja(tela, 160, ALTURA_BALCAO)
        desenhar_copo_americano(tela, 215, ALTURA_BALCAO)
        desenhar_copo_whisky(tela, 785, ALTURA_BALCAO)
        desenhar_whisky(tela, 850, ALTURA_BALCAO)

        self.escrever(tela, "Boteco Simulator", self.fonte_titulo, AMARELO, 90)
        self.escrever(tela, "A sinuca do boteco, agora no seu computador", self.fonte, BRANCO, 140)
        self.escrever(tela, f"Moedas: {moedas}", self.fonte_media, AMARELO, 550)

        self.botao_jogar.desenhar(tela, self.fonte_media)
        self.botao_loja.desenhar(tela, self.fonte_media)
        self.botao_instrucoes.desenhar(tela, self.fonte_media)
        self.botao_sair.desenhar(tela, self.fonte_media)

    def desenhar_instrucoes(self, tela):
        """Tela que explica como jogar."""
        tela.fill(FUNDO)
        self.escrever(tela, "Como jogar", self.fonte_titulo, AMARELO, 70)

        linhas = [
            "Mire movendo o mouse: a linha branca mostra onde a bola branca vai bater.",
            "Segure o botão esquerdo para carregar a força e solte para tacar.",
            "Cada fase tem um desafio escrito no topo da tela.",
            "Você tem um número limitado de tacadas para cumprir o desafio.",
            "Se a bola branca cair na caçapa, ela volta para o lugar inicial.",
            "Vencendo uma fase você ganha moedas para gastar na loja.",
            "ESC durante o jogo volta para o menu.",
        ]
        y = 150
        for linha in linhas:
            self.escrever(tela, linha, self.fonte, BRANCO, y)
            y += 40          # próxima linha 40 pixels pra baixo

        self.botao_voltar.desenhar(tela, self.fonte_media)

    def desenhar_loja(self, tela, moedas, melhorias):
        """Tela da loja: um botão por melhoria, com o preço ou COMPRADO."""
        tela.fill(FUNDO)
        self.escrever(tela, "Loja do Boteco", self.fonte_titulo, AMARELO, 60)
        self.escrever(tela, f"Suas moedas: {moedas}", self.fonte_media, AMARELO, 125)

        # Botão 0 é da melhoria 0, botão 1 da melhoria 1...
        for i in range(len(melhorias)):
            botao = self.botoes_loja[i]
            melhoria = melhorias[i]
            if melhoria.comprada:
                botao.texto = f"{melhoria.nome} - COMPRADO"
            else:
                botao.texto = f"{melhoria.nome} - {melhoria.preco} moedas"
            botao.desenhar(tela, self.fonte_media)
            self.escrever(tela, melhoria.descricao, self.fonte, BRANCO, botao.rect.bottom + 18)

        self.botao_voltar.desenhar(tela, self.fonte_media)

    def desenhar_fim(self, tela, moedas):
        """Tela de quando o jogador vence a última fase."""
        tela.fill(FUNDO)
        self.escrever(tela, "Você zerou o boteco!", self.fonte_titulo, AMARELO, 180)
        self.escrever(tela, "Todas as fases foram vencidas.", self.fonte_media, BRANCO, 270)
        self.escrever(tela, f"Total de moedas: {moedas}", self.fonte_media, AMARELO, 330)
        self.botao_voltar.desenhar(tela, self.fonte_media)
