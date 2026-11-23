"""
Classe Taco: a mira e a tacada.

O jogador mira com o mouse, segura o botão esquerdo para carregar a força
e solta para dar a tacada.

A mira funciona "andando" com um ponto invisível a partir da bola branca,
de 2 em 2 pixels, na direção do mouse, até ele encostar numa bola ou na
tabela. Nesse ponto desenhamos um círculo: é onde a branca vai estar
quando bater. Se bateu numa bola, também mostramos para onde ela vai.
"""

import pygame
from config import FORCA_MAXIMA, VELOCIDADE_CARGA, BRANCO, MADEIRA, AMARELO, VERMELHO

PASSO_MIRA = 2   # de quantos em quantos pixels o ponto da mira anda


class Taco:
    """Controla a mira, a força e o desenho do taco."""

    def __init__(self, tamanho_mira=3):
        """
        Args:
            tamanho_mira (int): quantas vezes esticar a linha que mostra
                para onde a bola atingida vai. Vai melhorar na loja.
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

    @staticmethod
    def achar_contato(bola_branca, d, bolas, rect_pano):
        """
        Anda com um ponto a partir da branca até encostar em algo.

        Args:
            bola_branca (Bola): a bola branca.
            d (pygame.Vector2): direção da tacada.
            bolas (list): todas as bolas da mesa.
            rect_pano (pygame.Rect): área do pano.

        Returns:
            tuple: (ponto, bola_atingida). bola_atingida é None se a
            mira encostou na tabela antes de qualquer bola.
        """
        r = bola_branca.raio
        ponto = pygame.Vector2(bola_branca.pos)
        while True:
            ponto += d * PASSO_MIRA     # dá um passinho na direção da tacada

            # Encostou numa bola? (distância entre centros menor que 2 raios)
            for bola in bolas:
                if bola is bola_branca or bola.encacapada:
                    continue
                if ponto.distance_to(bola.pos) <= 2 * r:
                    return ponto, bola

            # Encostou na tabela?
            if (ponto.x - r <= rect_pano.left or ponto.x + r >= rect_pano.right
                    or ponto.y - r <= rect_pano.top or ponto.y + r >= rect_pano.bottom):
                return ponto, None

    def desenhar(self, tela, bola_branca, pos_mouse, bolas, rect_pano):
        """
        Desenha a mira, o taco e a barra de força.

        Args:
            tela (pygame.Surface): onde desenhar.
            bola_branca (Bola): a bola que vai receber a tacada.
            pos_mouse (tuple): posição do mouse.
            bolas (list): todas as bolas da mesa.
            rect_pano (pygame.Rect): área do pano, para achar a tabela.
        """
        d = self.direcao(bola_branca, pos_mouse)
        ponto, alvo = self.achar_contato(bola_branca, d, bolas, rect_pano)

        # 1) Linha da branca até o ponto de contato + círculo vazado
        pygame.draw.line(tela, BRANCO, bola_branca.pos, ponto, 2)
        pygame.draw.circle(tela, BRANCO, ponto, bola_branca.raio, 2)

        # 2) Se vai bater numa bola, mostra para onde ela vai.
        #    Regra da sinuca: a bola atingida segue a reta que sai do
        #    círculo e passa pelo centro dela. Então só "esticamos" essa reta.
        if alvo is not None:
            seta = alvo.pos - ponto                  # do círculo até o centro da bola
            fim = alvo.pos + seta * self.tamanho_mira
            pygame.draw.line(tela, BRANCO, alvo.pos, fim, 2)

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