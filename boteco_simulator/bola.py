"""
Classe Bola: representa uma bola de sinuca.

Cada bola sabe sua posição, velocidade, cor e número.
Ela também sabe se mover, desacelerar pelo atrito e se desenhar.
"""

import pygame
from config import RAIO_BOLA, ATRITO, VELOCIDADE_MINIMA, BRANCO, PRETO


class Bola:
    """Uma bola de sinuca com posição, velocidade e cor."""

    def __init__(self, x, y, cor, numero=0):
        """
        Cria uma bola.

        Args:
            x (float): posição horizontal inicial.
            y (float): posição vertical inicial.
            cor (tuple): cor RGB da bola.
            numero (int): número da bola (0 = bola branca).
        """
        # pygame.Vector2 guarda dois números (x, y) e permite fazer contas
        # de vetor, como somar, multiplicar e medir comprimento.
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)   # começa parada
        self.cor = cor
        self.numero = numero
        self.raio = RAIO_BOLA
        self.encacapada = False           # vira True quando cai na caçapa
        self.tabelas = 0                  # quantas vezes bateu na tabela nesta tacada


    def esta_parada(self):
        """Retorna True se a bola estiver parada (ou já encaçapada)."""
        return self.encacapada or self.vel.length() == 0

    def atualizar(self):
        """Move a bola um quadro e aplica o atrito do pano."""
        if self.encacapada:
            return

        # Anda na direção da velocidade
        self.pos += self.vel

        # Atrito: a velocidade diminui um pouco a cada quadro
        self.vel *= ATRITO

        # Se ficou muito lenta, para de vez (senão ela "andaria" para sempre)
        if self.vel.length() < VELOCIDADE_MINIMA:
            self.vel = pygame.Vector2(0, 0)

    def desenhar(self, tela, fonte):
        """
        Desenha a bola na tela.

        Args:
            tela (pygame.Surface): onde desenhar.
            fonte (pygame.font.Font): fonte para escrever o número.
        """
        if self.encacapada:
            return

        centro = (int(self.pos.x), int(self.pos.y))

        # Sombra levemente deslocada para dar sensação de profundidade
        pygame.draw.circle(tela, (10, 60, 30), (centro[0] + 2, centro[1] + 2), self.raio)
        # Corpo da bola
        pygame.draw.circle(tela, self.cor, centro, self.raio)
        # Brilho pequeno no canto superior esquerdo
        pygame.draw.circle(tela, BRANCO, (centro[0] - 4, centro[1] - 4), 3)

        # Bolas numeradas ganham um círculo branco com o número no meio
        if self.numero > 0:
            pygame.draw.circle(tela, BRANCO, centro, 6)
            texto = fonte.render(str(self.numero), True, PRETO)
            tela.blit(texto, texto.get_rect(center=centro))