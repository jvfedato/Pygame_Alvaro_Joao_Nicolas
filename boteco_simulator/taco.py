"""
Classe Taco: a mira e a tacada.

O jogador mira com o mouse, segura o botão esquerdo para carregar a força
e solta para dar a tacada. O comprimento da linha de mira depende da
melhoria comprada na loja (vamos usar isso na etapa da loja).
"""

import pygame
from config import FORCA_MAXIMA, VELOCIDADE_CARGA, BRANCO, MADEIRA, AMARELO, VERMELHO


class Taco:
    """Controla a mira, a força e o desenho do taco."""

    def __init__(self, tamanho_mira=150):
        """
        Args:
            tamanho_mira (int): comprimento da linha de mira em pixels.
        """
        self.forca = 0.0
        self.carregando = False
        self.tamanho_mira = tamanho_mira

    @staticmethod
    def direcao(bola_branca, pos_mouse):
        """
        Calcula a direção (vetor de tamanho 1) da bola branca até o mouse.

        Returns:
            pygame.Vector2: direção da tacada.
        """
        d = pygame.Vector2(pos_mouse) - bola_branca.pos
        if d.length() == 0:
            return pygame.Vector2(1, 0)   # evita dividir por zero
        return d.normalize()

    def comecar_carga(self):
        """Chamado quando o jogador aperta o botão do mouse."""
        self.carregando = True
        self.forca = 0.0

    def atualizar(self):
        """Aumenta a força enquanto o botão estiver pressionado."""
        if self.carregando:
            self.forca = min(self.forca + VELOCIDADE_CARGA, FORCA_MAXIMA)

    def tacar(self, bola_branca, pos_mouse):
        """
        Dá a tacada: aplica a força na bola branca na direção do mouse.

        Returns:
            bool: True se a tacada teve força suficiente.
        """
        self.carregando = False
        if self.forca < 0.5:          # clique rápido demais, ignora
            self.forca = 0
            return False
        bola_branca.vel = self.direcao(bola_branca, pos_mouse) * self.forca
        self.forca = 0
        return True

    def desenhar(self, tela, bola_branca, pos_mouse):
        """Desenha a linha de mira, o taco e a barra de força."""
        d = self.direcao(bola_branca, pos_mouse)

        # Linha de mira tracejada: desenhamos vários pedacinhos
        for i in range(0, self.tamanho_mira, 12):
            inicio = bola_branca.pos + d * (bola_branca.raio + i)
            fim = bola_branca.pos + d * (bola_branca.raio + i + 6)
            pygame.draw.line(tela, BRANCO, inicio, fim, 2)

        # O taco fica do lado oposto da mira e recua conforme a força
        recuo = 15 + self.forca * 3
        ponta = bola_branca.pos - d * (bola_branca.raio + recuo)
        cabo = ponta - d * 220
        pygame.draw.line(tela, MADEIRA, ponta, cabo, 7)
        pygame.draw.line(tela, BRANCO, ponta, ponta - d * 8, 7)   # ponta clara do taco

        # Barra de força no canto inferior esquerdo
        largura_total = 200
        proporcao = self.forca / FORCA_MAXIMA
        pygame.draw.rect(tela, BRANCO, (20, 570, largura_total, 14), 2)
        # A cor vai de amarelo (fraco) para vermelho (forte)
        cor = (
            int(AMARELO[0] + (VERMELHO[0] - AMARELO[0]) * proporcao),
            int(AMARELO[1] + (VERMELHO[1] - AMARELO[1]) * proporcao),
            int(AMARELO[2] + (VERMELHO[2] - AMARELO[2]) * proporcao),
        )
        pygame.draw.rect(tela, cor, (22, 572, int((largura_total - 4) * proporcao), 10))