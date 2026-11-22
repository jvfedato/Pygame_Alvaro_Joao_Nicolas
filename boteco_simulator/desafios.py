"""
Desafios do Boteco Simulator (modo de um jogador).

Cada fase do jogo é um objeto Desafio. Existem 3 tipos:
  - "cacapa": encaçapar uma bola numa caçapa escolhida;
  - "tabela": encaçapar uma bola depois de ela bater na tabela;
  - "limpar": encaçapar todas as bolas.
"""

from bola import Bola
from config import BRANCO, CORES_BOLAS

POSICAO_BRANCA = (295, 300)   # onde a bola branca começa (x, y)


class Desafio:
    """Uma fase do jogo: as bolas, o objetivo e o limite de tacadas."""

    def __init__(self, tipo, descricao, posicoes, limite_tacadas, recompensa,
                 bola_alvo=0, cacapa_alvo=""):
        """
        Args:
            tipo (str): "cacapa", "tabela" ou "limpar".
            descricao (str): texto que aparece na tela explicando o objetivo.
            posicoes (list): lista de (numero, x, y) com as bolas da fase.
            limite_tacadas (int): quantas tacadas o jogador tem.
            recompensa (int): moedas ganhas ao vencer.
            bola_alvo (int): número da bola do objetivo (tipos cacapa e tabela).
            cacapa_alvo (str): nome da caçapa certa (só no tipo cacapa).
        """
        self.tipo = tipo
        self.descricao = descricao
        self.posicoes = posicoes
        self.limite_tacadas = limite_tacadas
        self.recompensa = recompensa
        self.bola_alvo = bola_alvo
        self.cacapa_alvo = cacapa_alvo

    def comecar(self):
        """
        Prepara a fase do zero e cria as bolas.

        Returns:
            list: as bolas da fase; a primeira é sempre a branca.
        """
        self.tacadas_restantes = self.limite_tacadas
        self.cumprido = False     # vira True quando o objetivo é feito
        self.errou = False        # vira True se a bola alvo cair do jeito errado

        self.bolas = [Bola(POSICAO_BRANCA[0], POSICAO_BRANCA[1], BRANCO, 0)]
        for numero, x, y in self.posicoes:
            self.bolas.append(Bola(x, y, CORES_BOLAS[numero], numero))
        return self.bolas

    def bola_caiu(self, bola, cacapa):
        """
        Avisa o desafio que uma bola numerada caiu na caçapa `cacapa`.
        Só importa se for a bola alvo.
        """
        if bola.numero != self.bola_alvo:
            return

        if self.tipo == "cacapa":
            if cacapa == self.cacapa_alvo:
                self.cumprido = True
            else:
                self.errou = True          # caiu na caçapa errada

        elif self.tipo == "tabela":
            if bola.tabelas > 0:
                self.cumprido = True
            else:
                self.errou = True          # caiu direto, sem bater na tabela

    def venceu(self):
        """Retorna True se o objetivo da fase foi cumprido."""
        if self.tipo == "limpar":
            # Venceu se nenhuma bola numerada sobrou na mesa
            for bola in self.bolas:
                if bola.numero > 0 and not bola.encacapada:
                    return False
            return True
        return self.cumprido

    def perdeu(self):
        """Retorna True se errou o objetivo ou acabaram as tacadas."""
        return self.errou or self.tacadas_restantes == 0


def criar_fases():
    """
    Cria a lista de fases, da mais fácil para a mais difícil.

    As posições estão em pixels. O pano verde vai de x=90 até x=910
    e de y=90 até y=510.

    Returns:
        list: lista de objetos Desafio.
    """
    fase1 = Desafio("cacapa", "Encaçape a bola 3 na caçapa de cima à direita",
                    [(3, 705, 195)],
                    limite_tacadas=3, recompensa=20,
                    bola_alvo=3, cacapa_alvo="sup_dir")

    fase2 = Desafio("cacapa", "Encaçape a bola 5 na caçapa de baixo no meio",
                    [(5, 500, 384), (8, 664, 258)],
                    limite_tacadas=3, recompensa=25,
                    bola_alvo=5, cacapa_alvo="inf_meio")

    fase3 = Desafio("tabela", "Encaçape a bola 2 indo de tabela (bater na borda antes)",
                    [(2, 418, 405)],
                    limite_tacadas=5, recompensa=35,
                    bola_alvo=2)

    fase4 = Desafio("limpar", "Limpe a mesa: encaçape todas as bolas",
                    [(1, 664, 300), (2, 697, 279), (3, 697, 321),
                     (4, 730, 258), (5, 730, 300), (6, 730, 342)],
                    limite_tacadas=10, recompensa=60)

    return [fase1, fase2, fase3, fase4]