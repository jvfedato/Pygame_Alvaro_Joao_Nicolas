# Pygame_Alvaro_Joao_Nicolas
Desenvolvimento do jogo em Python
a musica.mp3 veio do youtube - Boate azul - bruno e marrone
# 🎱 Boteco Simulator

Jogo de sinuca 2D feito em **Python com Pygame** para a disciplina de Design de Software (Desoft) do 1º semestre do Insper.

É um jogo de **um jogador só**: em vez de jogar contra alguém, você enfrenta uma sequência de **desafios de boteco** (encaçapar uma bola numa caçapa escolhida, acertar indo de tabela, limpar a mesa...). Cada desafio vencido dá **moedas**, que você gasta na **loja** comprando melhorias para a sua tacada.

## 👥 Autores

- Alvaro — *(nome completo)*
- João — *(nome completo)*
- Nicolas — *(nome completo)*

## ▶️ Como executar

1. Instale o Python 3 e o Pygame (só na primeira vez):
   ```bash
   python3 -m pip install pygame
   ```
2. Entre na pasta do jogo:
   ```bash
   cd boteco_simulator
   ```
3. Rode o arquivo principal, **`main.py`**:
   ```bash
   python3 main.py
   ```

## 🎮 Como jogar

| Ação | Comando |
|---|---|
| Mirar | Mover o mouse |
| Carregar a força | Segurar o botão esquerdo do mouse |
| Tacar | Soltar o botão |
| Continuar depois de uma fase | ENTER |
| Voltar ao menu | ESC |

- A **linha branca** mostra até onde a bola branca vai e o **círculo** mostra onde ela vai encostar. Se ela for bater numa bola, aparece também para onde essa bola vai.
- Cada fase tem um **limite de tacadas**. Se acabar, é só tentar de novo.
- Se a bola branca cair na caçapa, ela volta para o lugar inicial.

### Fases

| Fase | Desafio | Tacadas | Moedas |
|---|---|---|---|
| 1 | Encaçapar a bola 3 na caçapa de cima à direita | 3 | 20 |
| 2 | Encaçapar a bola 5 na caçapa de baixo no meio (com a 8 atrapalhando) | 3 | 25 |
| 3 | Encaçapar a bola 2 indo de tabela | 5 | 35 |
| 4 | Limpar a mesa (6 bolas) | 10 | 60 |

### Loja

| Melhoria | Preço | O que faz |
|---|---|---|
| RG de MAUÁ | 40 | A linha que mostra para onde a bola vai fica 2x maior |
| CERVEJA ORIGINAL 600ML | 60 | +1 tacada em todas as fases |
| FURTO DE BOTECO | 100 | Cada fase vencida dá o dobro de moedas |

## 📁 Organização do código

Cada arquivo cuida de uma parte do jogo, e cada um tem uma classe:

| Arquivo | O que faz |
|---|---|
| `main.py` | Arquivo principal. A classe `Jogo` junta tudo e roda o loop do jogo |
| `config.py` | Todas as constantes: tamanhos, cores, atrito, força |
| `bola.py` | Classe `Bola`: posição, velocidade, atrito e desenho |
| `mesa.py` | Classe `Mesa`: desenho da mesa e colisões (tabela, bolas, caçapas) |
| `taco.py` | Classe `Taco`: mira, força e tacada |
| `desafios.py` | Classe `Desafio` e a lista de fases |
| `loja.py` | Classes `Melhoria` e `Loja` |
| `telas.py` | Classes `Botao` e `Telas`: menu, instruções, loja e fim |
| `sons.py` | Classe `Sons`: efeitos sonoros e música |
| `assets/` | Arquivos de som |

## 🛠️ Design do jogo

*(Coloquem aqui os rascunhos, desenhos ou fotos das ideias do jogo: como pensaram nas fases, no visual do menu, na loja etc. A rubrica do objetivo 3 pede isso para o conceito A.)*

## 🔊 Créditos

- **Efeitos sonoros** (tacada, caçapa, vitória): gerados por programa, sem direitos autorais.
- **Música de fundo:** *Boate Azul* — Bruno & Marrone (retirada do YouTube).
- **Visual:** todo desenhado com formas do Pygame (retângulos, círculos e polígonos), sem imagens externas.

## 🤖 Uso de IA

O professor autorizou o uso de IA neste projeto. Usamos o Claude (Anthropic) como apoio para planejar o jogo, escrever partes do código, explicar o que cada parte faz e encontrar bugs. Todo o código foi lido, testado e ajustado pelo grupo, e sabemos explicar o que cada arquivo faz.