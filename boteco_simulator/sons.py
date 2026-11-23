"""
sons.py - Os sons do jogo

Carrega os arquivos da pasta assets uma vez só, quando o jogo abre.
Depois, pra tocar, é só fazer por exemplo: self.sons.tacada.play()
"""

import os
import pygame

# Caminho da pasta assets (fica do lado deste arquivo).
# Assim funciona tanto pelo terminal quanto pelo botão de play do VS Code.
PASTA_SONS = os.path.join(os.path.dirname(__file__), "assets")


class Sons:
    """Guarda os efeitos sonoros e a música."""

    def __init__(self):
        """Carrega os 3 efeitos e a música de fundo."""
        self.tacada = pygame.mixer.Sound(os.path.join(PASTA_SONS, "tacada.wav"))
        self.cacapa = pygame.mixer.Sound(os.path.join(PASTA_SONS, "cacapa.wav"))
        self.vitoria = pygame.mixer.Sound(os.path.join(PASTA_SONS, "vitoria.wav"))

        pygame.mixer.music.load(os.path.join(PASTA_SONS, "musica.mp3"))
        pygame.mixer.music.set_volume(0.3)     # volume de 0 a 1

    def tocar_musica(self):
        """Toca a música sem parar (o -1 quer dizer repetir pra sempre)."""
        pygame.mixer.music.play(-1)
