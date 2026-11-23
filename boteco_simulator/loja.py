"""
loja.py - A loja de melhorias

O jogador gasta as moedas das fases comprando melhorias.
Cada melhoria só pode ser comprada uma vez.
"""


class Melhoria:
    """Uma coisa que dá pra comprar na loja."""

    def __init__(self, nome, descricao, preco):
        """Começa sem estar comprada."""
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.comprada = False


class Loja:
    """Guarda as 3 melhorias e faz as compras."""

    def __init__(self):
        """Cria as melhorias com nome, explicação e preço."""
        self.mira_longa = Melhoria("Mira longa", "A linha que mostra para onde a bola vai fica 2x maior", 40)
        self.tacada_extra = Melhoria("Tacada extra", "Ganha +1 tacada em todas as fases", 60)
        self.moedas_dobro = Melhoria("Moedas em dobro", "Cada fase vencida dá o dobro de moedas", 100)

        # Mesma ordem dos botões na tela
        self.melhorias = [self.mira_longa, self.tacada_extra, self.moedas_dobro]

    def comprar(self, melhoria, moedas):
        """Tenta comprar e retorna quantas moedas sobraram."""
        if melhoria.comprada:
            return moedas            # já tem
        if moedas < melhoria.preco:
            return moedas            # não tem dinheiro
        melhoria.comprada = True
        return moedas - melhoria.preco
