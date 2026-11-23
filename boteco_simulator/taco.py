"""
taco.py - A classe Taco (mira e tacada)

Mira: um ponto sai da bola branca e vai andando de 2 em 2 pixels na direção
do mouse até encostar numa bola ou na tabela. Ali a gente desenha um círculo.
Tacada: segura o botão do mouse pra carregar a força e solta pra tacar.
"""

import pygame
from config import FORCA_MAXIMA, VELOCIDADE_CARGA, BRANCO, MADEIRA, AMARELO, VERMELHO

PASSO_MIRA = 2   # de quantos em quantos pixels o ponto da mira anda


class Taco:
    """O taco: guarda a força e desenha a mira."""

    def __init__(self, tamanho_mira=3):
        """tamanho_mira = quantas vezes esticar a linha da bola atingida (a loja aumenta)."""
        self.forca = 0
        self.carregando = False
        self.tamanho_mira = tamanho_mira

    def direcao(self, bola_branca, pos_mouse):
        """Seta de tamanho 1 que vai da bola branca até o mouse."""
        seta = pygame.Vector2(pos_mouse) - bola_branca.pos
        if seta.length() == 0:
            return pygame.Vector2(1, 0)   # mouse em cima da bola: evita dividir por zero
        return seta.normalize()

    def comecar_carga(self):
        """Apertou o botão do mouse: começa a carregar a força."""
        self.carregando = True
        self.forca = 0

    def atualizar(self):
        """Enquanto o botão está apertado, a força vai subindo até o máximo."""
        if self.carregando:
            self.forca = min(self.forca + VELOCIDADE_CARGA, FORCA_MAXIMA)

    def tacar(self, bola_branca, pos_mouse):
        """Soltou o botão: joga a bola branca na direção do mouse. Retorna True se tacou."""
        self.carregando = False
        if self.forca < 0.5:              # clique muito rápido, não conta
            self.forca = 0
            return False
        bola_branca.vel = self.direcao(bola_branca, pos_mouse) * self.forca
        self.forca = 0
        return True

    def achar_contato(self, bola_branca, direcao, bolas, rect_pano):
        """Anda com um ponto até encostar em algo. Retorna (ponto, bola) ou (ponto, None)."""
        r = bola_branca.raio
        ponto = pygame.Vector2(bola_branca.pos)
        while True:
            ponto += direcao * PASSO_MIRA     # um passinho pra frente

            # Encostou numa bola? (centros a menos de 2 raios de distância)
            for bola in bolas:
                if bola == bola_branca or bola.encacapada:
                    continue
                if ponto.distance_to(bola.pos) <= 2 * r:
                    return ponto, bola

            # Encostou na tabela?
            if (ponto.x - r <= rect_pano.left or ponto.x + r >= rect_pano.right
                    or ponto.y - r <= rect_pano.top or ponto.y + r >= rect_pano.bottom):
                return ponto, None

    def desenhar(self, tela, bola_branca, pos_mouse, bolas, rect_pano):
        """Desenha a mira, o taco e a barra de força."""
        direcao = self.direcao(bola_branca, pos_mouse)
        ponto, alvo = self.achar_contato(bola_branca, direcao, bolas, rect_pano)

        # Linha da branca até onde ela vai encostar + o círculo
        pygame.draw.line(tela, BRANCO, bola_branca.pos, ponto, 2)
        pygame.draw.circle(tela, BRANCO, ponto, bola_branca.raio, 2)

        # Se vai bater numa bola: ela vai na direção do círculo pro centro dela.
        # Então a gente pega essa seta e estica.
        if alvo is not None:
            seta = alvo.pos - ponto
            fim = alvo.pos + seta * self.tamanho_mira
            pygame.draw.line(tela, BRANCO, alvo.pos, fim, 2)

        # Taco: fica atrás da branca e vai pra trás quanto mais força
        recuo = 15 + self.forca * 3
        ponta = bola_branca.pos - direcao * (bola_branca.raio + recuo)
        cabo = ponta - direcao * 220
        pygame.draw.line(tela, MADEIRA, ponta, cabo, 7)
        pygame.draw.line(tela, BRANCO, ponta, ponta - direcao * 8, 7)    # pontinha clara

        # Barra de força no canto de baixo: amarela até a metade, depois vermelha
        proporcao = self.forca / FORCA_MAXIMA
        if proporcao < 0.5:
            cor = AMARELO
        else:
            cor = VERMELHO
        pygame.draw.rect(tela, BRANCO, (20, 570, 200, 14), 2)            # contorno
        pygame.draw.rect(tela, cor, (22, 572, int(196 * proporcao), 10))  # parte cheia
