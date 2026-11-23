"""
Sons do Boteco Simulator.

Carrega os arquivos da pasta assets uma vez só, no começo do jogo.
Depois é só chamar .play() no som que quiser.
"""

import os
import pygame

# Pasta "assets" que fica ao lado deste arquivo.
# Assim o jogo acha os sons de qualquer lugar de onde for executado.
PASTA_SONS = os.path.join(os.path.dirname(__file__), "assets")


class Sons:
    """Guarda todos os sons e a música de fundo."""

    def __init__(self):
        """Carrega os efeitos sonoros e prepara a música."""
        self.tacada = pygame.mixer.Sound(os.path.join(PASTA_SONS, "tacada.wav"))
        self.cacapa = pygame.mixer.Sound(os.path.join(PASTA_SONS, "cacapa.wav"))
        self.vitoria = pygame.mixer.Sound(os.path.join(PASTA_SONS, "vitoria.wav"))

        pygame.mixer.music.load(os.path.join(PASTA_SONS, "musica.mp3"))
        pygame.mixer.music.set_volume(0.3)     # música baixinha (0 a 1)

    def tocar_musica(self):
        """Toca a música de fundo sem parar (-1 = repetir para sempre)."""
        pygame.mixer.music.play(-1)