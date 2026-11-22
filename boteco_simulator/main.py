"""
Boteco Simulator - arquivo principal.

Execute este arquivo para jogar:  python main.py

Etapa 2: o jogo agora é uma sequência de desafios (fases).
Cada fase vencida dá moedas.
"""

import pygame
from config import LARGURA_TELA, ALTURA_TELA, FPS, TITULO, FUNDO, BRANCO, AMARELO, PRETO
from mesa import Mesa
from taco import Taco
from desafios import criar_fases, POSICAO_BRANCA


class Jogo:
    """Junta tudo: janela, mesa, taco, fases e o loop principal."""

    def __init__(self):
        """Inicia o pygame, cria a janela e começa a primeira fase."""
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()
        self.fonte_bola = pygame.font.SysFont("arial", 10, bold=True)
        self.fonte = pygame.font.SysFont("arial", 18, bold=True)
        self.fonte_grande = pygame.font.SysFont("arial", 40, bold=True)

        self.mesa = Mesa()
        self.taco = Taco()
        self.rodando = True

        self.fases = criar_fases()
        self.numero_fase = 0      # índice da fase atual na lista
        self.moedas = 0
        self.comecar_fase()

    def comecar_fase(self):
        """Coloca as bolas da fase atual na mesa."""
        self.desafio = self.fases[self.numero_fase]
        self.bolas = self.desafio.comecar()
        self.bola_branca = self.bolas[0]
        self.estado = "jogando"   # pode ser "jogando", "venceu" ou "perdeu"
        self.tacou = False        # True depois da tacada, até as bolas pararem

    def todas_paradas(self):
        """Retorna True se nenhuma bola estiver se mexendo."""
        for bola in self.bolas:
            if not bola.esta_parada():
                return False
        return True

    def tratar_eventos(self):
        """Lê teclado e mouse."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

            elif self.estado == "jogando":
                if evento.type == pygame.MOUSEBUTTONDOWN and self.todas_paradas():
                    self.taco.comecar_carga()
                elif evento.type == pygame.MOUSEBUTTONUP and self.taco.carregando:
                    if self.taco.tacar(self.bola_branca, pygame.mouse.get_pos()):
                        self.desafio.tacadas_restantes -= 1
                        self.tacou = True
                        for bola in self.bolas:
                            bola.tabelas = 0      # zera a contagem de tabelas

            # Fase acabou: ENTER continua
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                if self.estado == "venceu":
                    # vai para a próxima fase (depois da última, volta para a primeira)
                    self.numero_fase = (self.numero_fase + 1) % len(self.fases)
                self.comecar_fase()

    def atualizar(self):
        """Move as bolas, vê o que caiu e confere se a fase acabou."""
        for bola in self.bolas:
            if bola.encacapada:
                continue
            bola.atualizar()
            # Primeiro vê se caiu na caçapa; se não caiu, testa a tabela
            cacapa = self.mesa.verificar_cacapa(bola)
            if cacapa is None:
                if self.mesa.colidir_tabelas(bola):
                    bola.tabelas += 1
            elif bola != self.bola_branca:
                self.desafio.bola_caiu(bola, cacapa)

        # Testa cada par de bolas uma única vez
        for i in range(len(self.bolas)):
            for j in range(i + 1, len(self.bolas)):
                Mesa.colidir_bolas(self.bolas[i], self.bolas[j])

        # Depois da tacada, quando tudo parar, confere o resultado
        if self.tacou and self.todas_paradas():
            self.tacou = False

            # Se a branca caiu, ela volta para o começo
            if self.bola_branca.encacapada:
                self.bola_branca.encacapada = False
                self.bola_branca.pos = pygame.Vector2(POSICAO_BRANCA)

            if self.desafio.venceu():
                self.estado = "venceu"
                self.moedas += self.desafio.recompensa
            elif self.desafio.perdeu():
                self.estado = "perdeu"

    def desenhar_texto(self, texto, fonte, cor, x, y):
        """Escreve um texto com o centro no ponto (x, y)."""
        imagem = fonte.render(texto, True, cor)
        self.tela.blit(imagem, imagem.get_rect(center=(x, y)))

    def desenhar(self):
        """Desenha tudo na tela."""
        self.tela.fill(FUNDO)
        self.mesa.desenhar(self.tela)
        for bola in self.bolas:
            bola.desenhar(self.tela, self.fonte_bola)

        if self.estado == "jogando" and self.todas_paradas():
            self.taco.desenhar(self.tela, self.bola_branca, pygame.mouse.get_pos(),
                               self.bolas, self.mesa.rect_pano)

        # Informações no topo da tela
        titulo = f"Fase {self.numero_fase + 1}: {self.desafio.descricao}"
        self.tela.blit(self.fonte.render(titulo, True, BRANCO), (20, 20))
        info = f"Tacadas: {self.desafio.tacadas_restantes}    Moedas: {self.moedas}"
        self.tela.blit(self.fonte.render(info, True, AMARELO), (700, 20))

        # Caixa de fim de fase
        if self.estado != "jogando":
            pygame.draw.rect(self.tela, PRETO, (250, 200, 500, 200), border_radius=12)
            if self.estado == "venceu":
                self.desenhar_texto("Desafio cumprido!", self.fonte_grande, AMARELO, 500, 260)
                self.desenhar_texto(f"+{self.desafio.recompensa} moedas", self.fonte, BRANCO, 500, 310)
                self.desenhar_texto("ENTER para a próxima fase", self.fonte, BRANCO, 500, 350)
            else:
                self.desenhar_texto("Não foi dessa vez...", self.fonte_grande, BRANCO, 500, 270)
                self.desenhar_texto("ENTER para tentar de novo", self.fonte, BRANCO, 500, 340)

        pygame.display.flip()

    def executar(self):
        """Loop principal: eventos -> atualização -> desenho, 60 vezes por segundo."""
        while self.rodando:
            self.tratar_eventos()
            self.taco.atualizar()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)
        pygame.quit()


# Só roda o jogo se este arquivo for executado diretamente
if __name__ == "__main__":
    Jogo().executar()