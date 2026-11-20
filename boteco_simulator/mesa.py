"""
Classe Mesa: a mesa de sinuca.

Cuida do desenho da mesa, das caçapas e de toda a física de colisão:
bola com tabela, bola com bola e bola caindo na caçapa.
"""

import pygame
from config import (
    LARGURA_TELA, ALTURA_TELA, MARGEM_MESA, LARGURA_BORDA, RAIO_CACAPA,
    PERDA_TABELA, VERDE_PANO, MADEIRA, MADEIRA_ESCURA, PRETO,
)


class Mesa:
    """A mesa de sinuca: área de jogo, tabelas e caçapas."""

    def __init__(self):
        """Calcula os limites do pano e a posição das 6 caçapas."""
        # Retângulo da madeira (parte de fora da mesa)
        self.rect_madeira = pygame.Rect(
            MARGEM_MESA,
            MARGEM_MESA,
            LARGURA_TELA - 2 * MARGEM_MESA,
            ALTURA_TELA - 2 * MARGEM_MESA,
        )
        # Retângulo do pano verde (onde as bolas andam)
        self.rect_pano = self.rect_madeira.inflate(-2 * LARGURA_BORDA, -2 * LARGURA_BORDA)

        # As 6 caçapas: 4 cantos + 2 no meio das laterais compridas.
        # Cada caçapa recebe um nome para usarmos nos desafios depois.
        p = self.rect_pano
        self.cacapas = {
            "sup_esq": pygame.Vector2(p.left, p.top),
            "sup_meio": pygame.Vector2(p.centerx, p.top - 4),
            "sup_dir": pygame.Vector2(p.right, p.top),
            "inf_esq": pygame.Vector2(p.left, p.bottom),
            "inf_meio": pygame.Vector2(p.centerx, p.bottom + 4),
            "inf_dir": pygame.Vector2(p.right, p.bottom),
        }

    # ------------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------------
    def desenhar(self, tela):
        """Desenha madeira, pano e caçapas."""
        pygame.draw.rect(tela, MADEIRA_ESCURA, self.rect_madeira.inflate(10, 10), border_radius=18)
        pygame.draw.rect(tela, MADEIRA, self.rect_madeira, border_radius=14)
        pygame.draw.rect(tela, VERDE_PANO, self.rect_pano)

        for centro in self.cacapas.values():
            pygame.draw.circle(tela, PRETO, (int(centro.x), int(centro.y)), RAIO_CACAPA)

    # ------------------------------------------------------------------
    # Física
    # ------------------------------------------------------------------
    def colidir_tabelas(self, bola):
        """
        Faz a bola quicar se ela encostar na tabela.

        Returns:
            bool: True se a bola bateu na tabela neste quadro.
        """
        p = self.rect_pano
        bateu = False

        # Parede esquerda: se a bola passou do limite, empurra de volta
        # e inverte a velocidade horizontal (por isso o sinal de menos).
        if bola.pos.x - bola.raio < p.left:
            bola.pos.x = p.left + bola.raio
            bola.vel.x = -bola.vel.x * PERDA_TABELA
            bateu = True
        # Parede direita
        elif bola.pos.x + bola.raio > p.right:
            bola.pos.x = p.right - bola.raio
            bola.vel.x = -bola.vel.x * PERDA_TABELA
            bateu = True

        # Parede de cima: agora invertemos a velocidade vertical
        if bola.pos.y - bola.raio < p.top:
            bola.pos.y = p.top + bola.raio
            bola.vel.y = -bola.vel.y * PERDA_TABELA
            bateu = True
        # Parede de baixo
        elif bola.pos.y + bola.raio > p.bottom:
            bola.pos.y = p.bottom - bola.raio
            bola.vel.y = -bola.vel.y * PERDA_TABELA
            bateu = True

        return bateu

    def verificar_cacapa(self, bola):
        """
        Verifica se a bola caiu em alguma caçapa.

        Returns:
            str | None: o nome da caçapa onde caiu, ou None se não caiu.
        """
        for nome, centro in self.cacapas.items():
            # Se o centro da bola está dentro do buraco, ela caiu
            if bola.pos.distance_to(centro) < RAIO_CACAPA:
                bola.encacapada = True
                bola.vel = pygame.Vector2(0, 0)
                return nome
        return None

    @staticmethod
    def colidir_bolas(a, b):
        """
        Resolve a colisão entre duas bolas (choque elástico, mesma massa).

        Returns:
            bool: True se as bolas se encostaram neste quadro.
        """
        if a.encacapada or b.encacapada:
            return False

        diferenca = b.pos - a.pos          # vetor que vai do centro de A ao de B
        distancia = diferenca.length()
        soma_raios = a.raio + b.raio

        # Não estão encostando (ou estão exatamente no mesmo ponto)
        if distancia == 0 or distancia >= soma_raios:
            return False

        # "normal" = direção da linha que liga os dois centros, com tamanho 1
        normal = diferenca / distancia

        # 1) Separar as bolas para não ficarem uma dentro da outra
        sobreposicao = soma_raios - distancia
        a.pos -= normal * (sobreposicao / 2)
        b.pos += normal * (sobreposicao / 2)

        # 2) Trocar a parte da velocidade que está na direção da normal.
        #    Em bolas de mesma massa, num choque perfeito, elas "trocam"
        #    essa componente. A componente de lado continua igual.
        vel_relativa = a.vel - b.vel
        impacto = vel_relativa.dot(normal)   # produto escalar = quanto vai na direção da normal
        if impacto > 0:                       # só se estiverem se aproximando
            a.vel -= normal * impacto
            b.vel += normal * impacto
        return True