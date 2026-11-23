"""
desafios.py - As fases do jogo

Cada fase é um Desafio. Tem 3 tipos:
  "cacapa" -> encaçapar uma bola num buraco escolhido
  "tabela" -> encaçapar uma bola que bateu na borda antes
  "limpar" -> encaçapar todas as bolas
No final do arquivo, criar_fases() monta a lista com as 4 fases.
"""

from bola import Bola
from config import BRANCO, CORES_BOLAS

POSICAO_BRANCA = (295, 300)   # onde a bola branca começa


class Desafio:
    """Uma fase: as bolas, o objetivo e quantas tacadas o jogador tem."""

    def __init__(self, tipo, descricao, posicoes, limite_tacadas, recompensa,
                 bola_alvo=0, cacapa_alvo=""):
        """posicoes é uma lista de (numero, x, y). bola_alvo e cacapa_alvo dependem do tipo."""
        self.tipo = tipo
        self.descricao = descricao
        self.posicoes = posicoes
        self.limite_tacadas = limite_tacadas
        self.recompensa = recompensa
        self.bola_alvo = bola_alvo
        self.cacapa_alvo = cacapa_alvo

    def comecar(self):
        """Zera a fase e cria as bolas. A primeira da lista é sempre a branca."""
        self.tacadas_restantes = self.limite_tacadas
        self.cumprido = False     # True quando o jogador fez o objetivo
        self.errou = False        # True se a bola alvo caiu do jeito errado

        self.bolas = [Bola(POSICAO_BRANCA[0], POSICAO_BRANCA[1], BRANCO, 0)]
        for numero, x, y in self.posicoes:
            self.bolas.append(Bola(x, y, CORES_BOLAS[numero], numero))
        return self.bolas

    def bola_caiu(self, bola, cacapa):
        """O main avisa aqui quando uma bola cai. Só interessa se for a bola alvo."""
        if bola.numero != self.bola_alvo:
            return

        if self.tipo == "cacapa":
            if cacapa == self.cacapa_alvo:
                self.cumprido = True
            else:
                self.errou = True          # buraco errado

        elif self.tipo == "tabela":
            if bola.tabelas > 0:
                self.cumprido = True
            else:
                self.errou = True          # caiu direto, sem bater na borda

    def venceu(self):
        """Diz se o jogador cumpriu o objetivo."""
        if self.tipo == "limpar":
            # Se ainda tem alguma bola numerada na mesa, não venceu
            for bola in self.bolas:
                if bola.numero > 0 and not bola.encacapada:
                    return False
            return True
        return self.cumprido

    def perdeu(self):
        """Diz se o jogador errou o objetivo ou acabaram as tacadas."""
        return self.errou or self.tacadas_restantes == 0


def criar_fases():
    """Monta as 4 fases, da mais fácil pra mais difícil (o pano vai de x=90 a 910 e y=90 a 510)."""
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
