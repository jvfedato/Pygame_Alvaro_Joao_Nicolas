"""
mesa.py - A classe Mesa

Desenha a mesa (madeira, pano verde e as 6 caçapas) e cuida das batidas:
bola na tabela, bola na bola e bola caindo na caçapa.
"""

import pygame
from config import (LARGURA_TELA, ALTURA_TELA, MARGEM_MESA, LARGURA_BORDA, RAIO_CACAPA,
                    PERDA_TABELA, VERDE_PANO, MADEIRA, MADEIRA_ESCURA, PRETO)


class Mesa:
    """A mesa de sinuca."""

    def __init__(self):
        """Calcula onde fica o pano e onde fica cada caçapa."""
        # Retângulo da madeira (a mesa inteira)
        largura = LARGURA_TELA - 2 * MARGEM_MESA
        altura = ALTURA_TELA - 2 * MARGEM_MESA
        self.rect_madeira = pygame.Rect(MARGEM_MESA, MARGEM_MESA, largura, altura)

        # Retângulo do pano verde: a madeira encolhida pra dentro (onde as bolas andam)
        self.rect_pano = self.rect_madeira.inflate(-2 * LARGURA_BORDA, -2 * LARGURA_BORDA)

        # As 6 caçapas: 4 nos cantos e 2 no meio das laterais grandes
        p = self.rect_pano
        self.cacapas = {
            "sup_esq": pygame.Vector2(p.left, p.top),
            "sup_meio": pygame.Vector2(p.centerx, p.top - 4),
            "sup_dir": pygame.Vector2(p.right, p.top),
            "inf_esq": pygame.Vector2(p.left, p.bottom),
            "inf_meio": pygame.Vector2(p.centerx, p.bottom + 4),
            "inf_dir": pygame.Vector2(p.right, p.bottom),
        }

    def desenhar(self, tela):
        """Desenha a madeira, o pano e os buracos."""
        pygame.draw.rect(tela, MADEIRA_ESCURA, self.rect_madeira.inflate(10, 10), border_radius=18)
        pygame.draw.rect(tela, MADEIRA, self.rect_madeira, border_radius=14)
        pygame.draw.rect(tela, VERDE_PANO, self.rect_pano)

        for centro in self.cacapas.values():
            pygame.draw.circle(tela, PRETO, (int(centro.x), int(centro.y)), RAIO_CACAPA)

    def colidir_tabelas(self, bola):
        """Se a bola passou da borda, volta ela e inverte a direção. Retorna True se bateu."""
        p = self.rect_pano
        bateu = False

        # Bateu na esquerda ou na direita: inverte a velocidade no x
        if bola.pos.x - bola.raio < p.left:
            bola.pos.x = p.left + bola.raio
            bola.vel.x = -bola.vel.x * PERDA_TABELA
            bateu = True
        elif bola.pos.x + bola.raio > p.right:
            bola.pos.x = p.right - bola.raio
            bola.vel.x = -bola.vel.x * PERDA_TABELA
            bateu = True

        # Bateu em cima ou embaixo: inverte a velocidade no y
        if bola.pos.y - bola.raio < p.top:
            bola.pos.y = p.top + bola.raio
            bola.vel.y = -bola.vel.y * PERDA_TABELA
            bateu = True
        elif bola.pos.y + bola.raio > p.bottom:
            bola.pos.y = p.bottom - bola.raio
            bola.vel.y = -bola.vel.y * PERDA_TABELA
            bateu = True

        return bateu

    def verificar_cacapa(self, bola):
        """Vê se a bola caiu em algum buraco. Retorna o nome do buraco ou None."""
        for nome, centro in self.cacapas.items():
            # O centro da bola entrou no buraco? Então caiu
            if bola.pos.distance_to(centro) < RAIO_CACAPA:
                bola.encacapada = True
                bola.vel = pygame.Vector2(0, 0)
                return nome
        return None

    def colidir_bolas(self, a, b):
        """Faz duas bolas baterem uma na outra, se estiverem encostando."""
        if a.encacapada or b.encacapada:
            return

        diferenca = b.pos - a.pos          # seta do centro da A até o centro da B
        distancia = diferenca.length()
        soma_raios = a.raio + b.raio

        # Longe demais (ou exatamente no mesmo lugar): não bateram
        if distancia == 0 or distancia >= soma_raios:
            return

        # Direção da linha que liga os dois centros (seta de tamanho 1)
        direcao = diferenca / distancia

        # 1) Afasta as duas pra não ficarem uma dentro da outra
        entrou = soma_raios - distancia
        a.pos -= direcao * (entrou / 2)
        b.pos += direcao * (entrou / 2)

        # 2) Troca a velocidade na direção da linha entre os centros.
        #    O .dot (produto escalar) mede quanto da velocidade vai nessa direção.
        empurrao = (a.vel - b.vel).dot(direcao)
        if empurrao > 0:                   # só se estiverem indo uma contra a outra
            a.vel -= direcao * empurrao
            b.vel += direcao * empurrao
