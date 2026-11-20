"""
Classe Taco: a mira e a tacada.

O jogador mira com o mouse, segura o botão esquerdo para carregar a força
e solta para dar a tacada.

A mira usa a técnica da "bola fantasma": calculamos onde a bola branca
vai estar no instante em que encostar na primeira bola do caminho e
desenhamos um círculo ali. A partir desse ponto mostramos:
  - para onde a bola atingida vai (linha que sai dela);
  - para onde a bola branca desvia depois do choque (linha curta).
O comprimento dessas linhas (tamanho_mira) vai poder ser melhorado na loja.
"""

import math
import pygame
from config import FORCA_MAXIMA, VELOCIDADE_CARGA, BRANCO, MADEIRA, AMARELO, VERMELHO


class Taco:
    """Controla a mira, a força e o desenho do taco."""

    def __init__(self, tamanho_mira=80):
        """
        Args:
            tamanho_mira (int): comprimento da linha que mostra para onde
                a bola atingida vai (em pixels).
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

    # ------------------------------------------------------------------
    # Cálculo da mira
    # ------------------------------------------------------------------
    @staticmethod
    def primeira_bola_no_caminho(bola_branca, d, bolas):
        """
        Descobre qual bola a branca vai acertar primeiro andando na direção d.

        Ideia: a branca encosta numa bola quando a distância entre os
        centros fica igual a 2 raios. Então "inflamos" cada bola para
        raio 2R e vemos onde a reta da tacada entra nesse círculo maior.

        Returns:
            tuple: (bola_atingida, distancia_percorrida) ou (None, None).
        """
        melhor_bola = None
        melhor_t = None
        for bola in bolas:
            if bola is bola_branca or bola.encacapada:
                continue
            m = bola.pos - bola_branca.pos      # vetor da branca até a bola
            proj = m.dot(d)                     # quanto dessa distância está "na frente"
            if proj <= 0:
                continue                        # bola está atrás, não tem como acertar
            # distância (ao quadrado) entre o centro da bola e a reta da tacada
            perp2 = m.length_squared() - proj ** 2
            alcance2 = (2 * bola.raio) ** 2
            if perp2 > alcance2:
                continue                        # a reta passa longe demais
            # Pitágoras: recua do ponto mais próximo até onde encosta
            t = proj - math.sqrt(alcance2 - perp2)
            if melhor_t is None or t < melhor_t:
                melhor_bola, melhor_t = bola, t
        return melhor_bola, melhor_t

    @staticmethod
    def distancia_ate_tabela(bola_branca, d, rect_pano):
        """
        Calcula quanto a branca anda na direção d até encostar na tabela.

        Returns:
            float: distância em pixels.
        """
        r = bola_branca.raio
        tempos = []
        # Para cada eixo, quanto falta até a parede dividido pela velocidade nesse eixo
        if d.x > 0:
            tempos.append((rect_pano.right - r - bola_branca.pos.x) / d.x)
        elif d.x < 0:
            tempos.append((rect_pano.left + r - bola_branca.pos.x) / d.x)
        if d.y > 0:
            tempos.append((rect_pano.bottom - r - bola_branca.pos.y) / d.y)
        elif d.y < 0:
            tempos.append((rect_pano.top + r - bola_branca.pos.y) / d.y)
        return max(0, min(tempos))

    # ------------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------------
    def desenhar(self, tela, bola_branca, pos_mouse, bolas, rect_pano):
        """
        Desenha a mira (com bola fantasma), o taco e a barra de força.

        Args:
            tela (pygame.Surface): onde desenhar.
            bola_branca (Bola): a bola que vai receber a tacada.
            pos_mouse (tuple): posição do mouse.
            bolas (list): todas as bolas da mesa.
            rect_pano (pygame.Rect): área do pano, para achar a tabela.
        """
        d = self.direcao(bola_branca, pos_mouse)
        alvo, t_bola = self.primeira_bola_no_caminho(bola_branca, d, bolas)
        t_tabela = self.distancia_ate_tabela(bola_branca, d, rect_pano)

        # Se a tabela vem antes de qualquer bola, a mira para na tabela
        if alvo is None or t_tabela < t_bola:
            alvo = None
            t = t_tabela
        else:
            t = t_bola

        # Posição da "bola fantasma": onde a branca estará no momento do choque
        fantasma = bola_branca.pos + d * t

        # 1) Linha da branca até a bola fantasma + o círculo vazado
        pygame.draw.line(tela, BRANCO, bola_branca.pos, fantasma, 2)
        pygame.draw.circle(tela, BRANCO, fantasma, bola_branca.raio, 2)

        if alvo is not None:
            # "normal" = direção do centro da fantasma até o centro do alvo.
            # É exatamente para lá que a bola atingida vai.
            normal = (alvo.pos - fantasma).normalize()

            # 2) Linha que sai da bola atingida
            pygame.draw.line(tela, BRANCO, alvo.pos, alvo.pos + normal * self.tamanho_mira, 2)

            # 3) Desvio da branca: tiramos de d a parte que foi para o alvo.
            #    O que sobra é perpendicular à normal (regra das bolas iguais).
            desvio = d - normal * d.dot(normal)
            if desvio.length() > 0.01:
                desvio = desvio.normalize() * (self.tamanho_mira * 0.5)
                pygame.draw.line(tela, BRANCO, fantasma, fantasma + desvio, 2)

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