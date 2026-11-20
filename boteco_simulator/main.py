"""
Boteco Simulator - arquivo principal.

Execute este arquivo para jogar:  python main.py

Nesta etapa 1 temos: a mesa, as bolas, a física e a tacada com o mouse.
Nas próximas etapas vamos adicionar desafios, moedas, loja, telas e sons.
"""

import pygame
from config import LARGURA_TELA, ALTURA_TELA, FPS, TITULO, FUNDO, BRANCO, CORES_BOLAS, RAIO_BOLA
from bola import Bola
from mesa import Mesa
from taco import Taco


class Jogo:
    """Junta tudo: janela, mesa, bolas, taco e o loop principal."""

    def __init__(self):
        """Inicia o pygame, cria a janela e monta a mesa."""
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()        # controla o FPS
        self.fonte_bola = pygame.font.SysFont("arial", 10, bold=True)
        self.fonte = pygame.font.SysFont("arial", 20, bold=True)

        self.mesa = Mesa()
        self.taco = Taco()
        self.rodando = True
        self.tacadas = 0
        self.montar_bolas()

    def montar_bolas(self):
        """Coloca a bola branca e as bolas numeradas num triângulo."""
        pano = self.mesa.rect_pano
        # Bola branca a 1/4 da mesa, na altura do meio
        self.bola_branca = Bola(pano.left + pano.width * 0.25, pano.centery, BRANCO, 0)
        self.bolas = [self.bola_branca]

        # Triângulo: fileira 1 tem 1 bola, fileira 2 tem 2... até 4 fileiras (10 lugares)
        x_inicio = pano.left + pano.width * 0.7
        numero = 1
        for fileira in range(4):
            for i in range(fileira + 1):
                if numero > 8:
                    break
                x = x_inicio + fileira * (RAIO_BOLA * 2 - 2)
                y = pano.centery + (i - fileira / 2) * (RAIO_BOLA * 2 + 1)
                self.bolas.append(Bola(x, y, CORES_BOLAS[numero], numero))
                numero += 1

    def todas_paradas(self):
        """Retorna True se nenhuma bola estiver se mexendo."""
        return all(b.esta_parada() for b in self.bolas)

    def tratar_eventos(self):
        """Lê teclado e mouse."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            # Só deixamos tacar quando tudo parou
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.todas_paradas():
                    self.taco.comecar_carga()
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.taco.carregando:
                    if self.taco.tacar(self.bola_branca, pygame.mouse.get_pos()):
                        self.tacadas += 1

    def atualizar_fisica(self):
        """Move as bolas e resolve todas as colisões."""
        for bola in self.bolas:
            bola.atualizar()
            self.mesa.colidir_tabelas(bola)

        # Testa cada par de bolas uma única vez (i com j, sendo j > i)
        for i in range(len(self.bolas)):
            for j in range(i + 1, len(self.bolas)):
                Mesa.colidir_bolas(self.bolas[i], self.bolas[j])

        for bola in self.bolas:
            if not bola.encacapada:
                self.mesa.verificar_cacapa(bola)

        # Se a branca caiu, ela volta para o ponto inicial
        if self.bola_branca.encacapada and self.todas_paradas():
            pano = self.mesa.rect_pano
            self.bola_branca.encacapada = False
            self.bola_branca.pos = pygame.Vector2(pano.left + pano.width * 0.25, pano.centery)

    def desenhar(self):
        """Desenha tudo na tela."""
        self.tela.fill(FUNDO)
        self.mesa.desenhar(self.tela)
        for bola in self.bolas:
            bola.desenhar(self.tela, self.fonte_bola)

        # Só mostra o taco quando dá para tacar
        if self.todas_paradas():
            self.taco.desenhar(self.tela, self.bola_branca, pygame.mouse.get_pos())

        texto = self.fonte.render(f"Tacadas: {self.tacadas}", True, BRANCO)
        self.tela.blit(texto, (20, 20))
        pygame.display.flip()   # mostra na tela o que foi desenhado

    def executar(self):
        """Loop principal: eventos -> atualização -> desenho, 60 vezes por segundo."""
        while self.rodando:
            self.tratar_eventos()
            self.taco.atualizar()
            self.atualizar_fisica()
            self.desenhar()
            self.relogio.tick(FPS)
        pygame.quit()


# Só roda o jogo se este arquivo for executado diretamente
if __name__ == "__main__":
    Jogo().executar()