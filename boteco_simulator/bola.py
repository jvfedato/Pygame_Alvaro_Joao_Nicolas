"""
bola.py - A classe Bola

Cada bola guarda onde ela está (pos), pra onde e quão rápido ela vai (vel),
a cor e o número. A bola sabe andar, frear e se desenhar na tela.
"""

import pygame
from config import RAIO_BOLA, ATRITO, VELOCIDADE_MINIMA, BRANCO, PRETO


class Bola:
    """Uma bola de sinuca."""

    def __init__(self, x, y, cor, numero=0):
        """Cria a bola parada no ponto (x, y). Número 0 é a bola branca."""
        # Vector2 guarda x e y juntos e deixa a gente somar e multiplicar fácil
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.cor = cor
        self.numero = numero
        self.raio = RAIO_BOLA
        self.encacapada = False      # vira True quando cai num buraco
        self.tabelas = 0             # quantas vezes bateu na tabela nessa tacada

    def esta_parada(self):
        """Diz se a bola está parada (ou se já caiu)."""
        return self.encacapada or self.vel.length() == 0

    def mover(self, fracao):
        """Anda um pedaço do caminho (fracao = 0.1 anda um décimo do quadro)."""
        self.pos += self.vel * fracao

    def frear(self):
        """Diminui a velocidade por causa do atrito do pano."""
        if self.encacapada:
            return

        self.vel *= ATRITO

        # Se ficou muito devagar, para de vez (senão nunca chegaria a zero)
        if self.vel.length() < VELOCIDADE_MINIMA:
            self.vel = pygame.Vector2(0, 0)

    def desenhar(self, tela, fonte):
        """Desenha a bola com sombra, brilho e o número."""
        if self.encacapada:
            return

        x = int(self.pos.x)
        y = int(self.pos.y)

        pygame.draw.circle(tela, (10, 60, 30), (x + 2, y + 2), self.raio)   # sombra
        pygame.draw.circle(tela, self.cor, (x, y), self.raio)               # bola
        pygame.draw.circle(tela, BRANCO, (x - 4, y - 4), 3)                 # brilho

        # Bola com número: bolinha branca no meio com o número escrito
        if self.numero > 0:
            pygame.draw.circle(tela, BRANCO, (x, y), 6)
            texto = fonte.render(str(self.numero), True, PRETO)
            tela.blit(texto, texto.get_rect(center=(x, y)))
