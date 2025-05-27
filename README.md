# verificador-robocode-2025

## Scripts disponíveis

### 1. somatoria.py
Gera os resultados oficiais das equipes de cada chave (A e B) a partir dos arquivos de partidas CSV.

- Lê todos os arquivos da pasta `partidas/`.
- Soma os pontos e estatísticas de cada equipe, agrupando por chave (A ou B).
- Apenas o 1º lugar de cada partida recebe 5 pontos.
- Gera dois arquivos de saída:
  - `resultado_chave_a.csv`
  - `resultado_chave_b.csv`
- Cada arquivo contém: POSICAO, EQUIPE, SOMA PONTOS, JOGOS, VITORIA, DERROTA, GP, GC, SG, %

### 2. verifica_jogos.py
Verifica se todas as equipes participaram exatamente de 13 partidas e identifica possíveis erros de contagem.

- Conta em quantos arquivos de partidas cada equipe aparece.
- Mostra um relatório com o número de jogos de cada equipe.
- Se alguma equipe tiver diferente de 13 jogos, exibe a lista de arquivos em que essa equipe aparece, facilitando a auditoria.

## Como usar

1. Coloque todos os arquivos de partidas na pasta `partidas/`.
2. Execute `somatoria.py` para gerar os resultados oficiais das chaves.
3. Execute `verifica_jogos.py` para conferir se todas as equipes têm 13 jogos e, se houver erro, ver em quais arquivos está o problema.

## Dependências

Instale as dependências com:

```
pip install -r requirements.txt
```
