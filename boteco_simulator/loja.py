"""
Loja do Boteco Simulator.

O jogador gasta as moedas ganhas nas fases para comprar melhorias.
Cada melhoria só pode ser comprada uma vez.
"""


class Melhoria:
    """Uma melhoria que pode ser comprada na loja."""

    def __init__(self, nome, descricao, preco):
        """
        Args:
            nome (str): nome que aparece no botão.
            descricao (str): explicação curta do que a melhoria faz.
            preco (int): quantas moedas custa.
        """
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.comprada = False


class Loja:
    """Guarda as melhorias e cuida das compras."""

    def __init__(self):
        """Cria as 3 melhorias do jogo."""
        self.mira_longa = Melhoria("Mira longa", "A linha que mostra para onde a bola vai fica 2x maior", 40)
        self.tacada_extra = Melhoria("Tacada extra", "Ganha +1 tacada em todas as fases", 60)
        self.moedas_dobro = Melhoria("Moedas em dobro", "Cada fase vencida dá o dobro de moedas", 100)

        # Lista com as 3, na ordem em que aparecem na tela
        self.melhorias = [self.mira_longa, self.tacada_extra, self.moedas_dobro]

    def comprar(self, melhoria, moedas):
        """
        Tenta comprar uma melhoria.

        Args:
            melhoria (Melhoria): a melhoria escolhida.
            moedas (int): quantas moedas o jogador tem.

        Returns:
            int: quantas moedas sobraram depois da compra
            (se não deu para comprar, devolve o mesmo valor).
        """
        if melhoria.comprada:
            return moedas            # já tem, não compra de novo
        if moedas < melhoria.preco:
            return moedas            # dinheiro não dá
        melhoria.comprada = True
        return moedas - melhoria.preco
