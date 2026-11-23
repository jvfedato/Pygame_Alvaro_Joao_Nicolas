"""
main.py - Arquivo principal do Boteco Simulator (é esse que roda o jogo)

Para jogar: python3 main.py

A classe Jogo junta tudo: a janela, as telas, a mesa, o taco, as fases,
a loja e os sons. O loop do jogo roda 60 vezes por segundo e faz sempre
3 coisas: lê o mouse/teclado, atualiza as bolas e desenha a tela.
"""

import pygame
from config import (LARGURA_TELA, ALTURA_TELA, FPS, TITULO, FUNDO, BRANCO, AMARELO, PRETO,
                    PASSOS_POR_QUADRO)
from mesa import Mesa
from taco import Taco
from desafios import criar_fases, POSICAO_BRANCA
from telas import Telas
from sons import Sons
from loja import Loja


class Jogo:
    """O jogo inteiro."""

    def __init__(self):
        """Abre a janela, cria tudo e começa no menu."""
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()
        self.fonte_bola = pygame.font.SysFont("arial", 10, bold=True)
        self.fonte = pygame.font.SysFont("arial", 18, bold=True)
        self.fonte_grande = pygame.font.SysFont("arial", 40, bold=True)

        self.mesa = Mesa()
        self.taco = Taco()
        self.telas = Telas()
        self.sons = Sons()
        self.sons.tocar_musica()
        self.loja = Loja()
        self.rodando = True

        self.fases = criar_fases()
        self.numero_fase = 0      # posição da fase atual na lista (0 = fase 1)
        self.moedas = 0
        self.moedas_ganhas = 0    # quanto ganhou na última fase
        self.tela_atual = "menu"  # "menu", "instrucoes", "loja", "jogo" ou "fim"

    def comecar_fase(self):
        """Coloca as bolas da fase atual na mesa."""
        self.desafio = self.fases[self.numero_fase]
        self.bolas = self.desafio.comecar()
        self.bola_branca = self.bolas[0]
        self.estado = "jogando"   # "jogando", "venceu" ou "perdeu"
        self.tacou = False        # fica True da tacada até as bolas pararem

        # Melhoria da loja: +1 tacada
        if self.loja.tacada_extra.comprada:
            self.desafio.tacadas_restantes += 1

    def todas_paradas(self):
        """Diz se todas as bolas pararam."""
        for bola in self.bolas:
            if not bola.esta_parada():
                return False
        return True

    # --- Mouse e teclado ---

    def tratar_eventos(self):
        """Pega cada evento e manda pra tela que está aberta."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif self.tela_atual == "menu":
                self.eventos_menu(evento)
            elif self.tela_atual == "instrucoes" or self.tela_atual == "fim":
                if self.telas.botao_voltar.foi_clicado(evento):
                    self.tela_atual = "menu"
            elif self.tela_atual == "loja":
                self.eventos_loja(evento)
            elif self.tela_atual == "jogo":
                self.eventos_jogo(evento)

    def eventos_menu(self, evento):
        """Cliques nos botões do menu."""
        if self.telas.botao_jogar.foi_clicado(evento):
            self.numero_fase = 0
            self.comecar_fase()
            self.tela_atual = "jogo"
        elif self.telas.botao_loja.foi_clicado(evento):
            self.tela_atual = "loja"
        elif self.telas.botao_instrucoes.foi_clicado(evento):
            self.tela_atual = "instrucoes"
        elif self.telas.botao_sair.foi_clicado(evento):
            self.rodando = False

    def eventos_loja(self, evento):
        """Cliques na loja: comprar ou voltar."""
        if self.telas.botao_voltar.foi_clicado(evento):
            self.tela_atual = "menu"

        for i in range(len(self.loja.melhorias)):
            if self.telas.botoes_loja[i].foi_clicado(evento):
                antes = self.moedas
                self.moedas = self.loja.comprar(self.loja.melhorias[i], self.moedas)
                if self.moedas < antes:            # se gastou, é porque comprou
                    self.sons.vitoria.play()

        # Melhoria da loja: mira mais comprida
        if self.loja.mira_longa.comprada:
            self.taco.tamanho_mira = 6

    def eventos_jogo(self, evento):
        """Na mesa: mouse pra tacar, ENTER pra continuar, ESC pra voltar ao menu."""
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.tela_atual = "menu"

        elif self.estado == "jogando":
            if evento.type == pygame.MOUSEBUTTONDOWN and self.todas_paradas():
                self.taco.comecar_carga()
            elif evento.type == pygame.MOUSEBUTTONUP and self.taco.carregando:
                if self.taco.tacar(self.bola_branca, pygame.mouse.get_pos()):
                    self.sons.tacada.play()
                    self.desafio.tacadas_restantes -= 1
                    self.tacou = True
                    for bola in self.bolas:
                        bola.tabelas = 0      # começa a contar as tabelas de novo

        # A fase acabou: ENTER pra seguir
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            if self.estado == "perdeu":
                self.comecar_fase()                     # tenta de novo
            elif self.numero_fase == len(self.fases) - 1:
                self.tela_atual = "fim"                 # era a última fase
            else:
                self.numero_fase += 1                   # próxima fase
                self.comecar_fase()

    # --- Física ---

    def atualizar(self):
        """Move as bolas, vê o que bateu e o que caiu, e confere se a fase acabou."""
        # As bolas andam em 10 passinhos por quadro. Assim, numa tacada forte,
        # a branca não "pula" pra dentro de outra bola.
        for passo in range(PASSOS_POR_QUADRO):
            for bola in self.bolas:
                if bola.encacapada:
                    continue
                bola.mover(1 / PASSOS_POR_QUADRO)

                # Primeiro vê se caiu no buraco. Se não caiu, vê se bateu na tabela.
                cacapa = self.mesa.verificar_cacapa(bola)
                if cacapa is None:
                    if self.mesa.colidir_tabelas(bola):
                        bola.tabelas += 1
                else:
                    self.sons.cacapa.play()
                    if bola != self.bola_branca:
                        self.desafio.bola_caiu(bola, cacapa)

            # Testa cada par de bolas uma vez só (a 0 com a 1, a 0 com a 2...)
            for i in range(len(self.bolas)):
                for j in range(i + 1, len(self.bolas)):
                    self.mesa.colidir_bolas(self.bolas[i], self.bolas[j])

        # Atrito: uma vez por quadro, depois dos passinhos
        for bola in self.bolas:
            bola.frear()

        # Depois da tacada, quando tudo parar, vê como ficou
        if self.tacou and self.todas_paradas():
            self.tacou = False

            # A branca caiu? Volta pro lugar do começo
            if self.bola_branca.encacapada:
                self.bola_branca.encacapada = False
                self.bola_branca.pos = pygame.Vector2(POSICAO_BRANCA)

            if self.desafio.venceu():
                self.estado = "venceu"
                self.moedas_ganhas = self.desafio.recompensa
                if self.loja.moedas_dobro.comprada:        # melhoria da loja
                    self.moedas_ganhas = self.moedas_ganhas * 2
                self.moedas += self.moedas_ganhas
                self.sons.vitoria.play()
            elif self.desafio.perdeu():
                self.estado = "perdeu"

    # --- Desenho ---

    def desenhar_texto(self, texto, fonte, cor, x, y):
        """Escreve um texto com o centro no ponto (x, y)."""
        imagem = fonte.render(texto, True, cor)
        self.tela.blit(imagem, imagem.get_rect(center=(x, y)))

    def desenhar_jogo(self):
        """Desenha a mesa, as bolas, o taco e as informações em cima."""
        self.tela.fill(FUNDO)
        self.mesa.desenhar(self.tela)
        for bola in self.bolas:
            bola.desenhar(self.tela, self.fonte_bola)

        # O taco só aparece quando dá pra tacar
        if self.estado == "jogando" and self.todas_paradas():
            self.taco.desenhar(self.tela, self.bola_branca, pygame.mouse.get_pos(),
                               self.bolas, self.mesa.rect_pano)

        # Texto do topo: fase, objetivo, tacadas e moedas
        titulo = f"Fase {self.numero_fase + 1}: {self.desafio.descricao}"
        self.tela.blit(self.fonte.render(titulo, True, BRANCO), (20, 20))
        info = f"Tacadas: {self.desafio.tacadas_restantes}    Moedas: {self.moedas}"
        self.tela.blit(self.fonte.render(info, True, AMARELO), (700, 20))

        # Caixa preta de quando a fase acaba
        if self.estado != "jogando":
            pygame.draw.rect(self.tela, PRETO, (250, 200, 500, 200), border_radius=12)
            if self.estado == "venceu":
                self.desenhar_texto("Desafio cumprido!", self.fonte_grande, AMARELO, 500, 260)
                self.desenhar_texto(f"+{self.moedas_ganhas} moedas", self.fonte, BRANCO, 500, 310)
                self.desenhar_texto("ENTER para continuar", self.fonte, BRANCO, 500, 350)
            else:
                self.desenhar_texto("Não foi dessa vez...", self.fonte_grande, BRANCO, 500, 270)
                self.desenhar_texto("ENTER para tentar de novo", self.fonte, BRANCO, 500, 340)

    def desenhar(self):
        """Desenha a tela que está aberta e mostra na janela."""
        if self.tela_atual == "menu":
            self.telas.desenhar_menu(self.tela, self.moedas)
        elif self.tela_atual == "instrucoes":
            self.telas.desenhar_instrucoes(self.tela)
        elif self.tela_atual == "loja":
            self.telas.desenhar_loja(self.tela, self.moedas, self.loja.melhorias)
        elif self.tela_atual == "fim":
            self.telas.desenhar_fim(self.tela, self.moedas)
        else:
            self.desenhar_jogo()
        pygame.display.flip()

    def executar(self):
        """O loop do jogo: eventos -> atualizar -> desenhar, 60 vezes por segundo."""
        while self.rodando:
            self.tratar_eventos()
            if self.tela_atual == "jogo":
                self.taco.atualizar()
                self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)
        pygame.quit()


# Só começa o jogo se esse arquivo for o que foi executado
if __name__ == "__main__":
    Jogo().executar()
