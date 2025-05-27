import os
import re
import time

start_time = time.time()
print(f"Iniciando verificação de jogos em {time.strftime('%H:%M:%S')}")

EQUIPES = [
    'SemNomeMasFunciona',
    'Uniao_Flasco',
    'bppd',
    'Xi_Beeu_z40',
    'Compilou_apanhou',
    'OS_DIGITJA_RAPDICO',
    'Os_Fuscoes',
    'Os_Fieis',
    'os_decanos',
    'CARIJOS_DA_PAMONHATRONICA',
]

jogos_por_equipe = {equipe: 0 for equipe in EQUIPES}
arquivos_por_equipe = {equipe: [] for equipe in EQUIPES}

partidas_dir = 'partidas'
for arquivo in os.listdir(partidas_dir):
    if not arquivo.endswith('.csv'):
        continue
    with open(os.path.join(partidas_dir, arquivo), 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    # Pega apenas as linhas dos robôs
    dados_robos = [l.strip() for l in linhas if re.match(r'^[0-9]+(st|nd|rd|th),', l.strip())]
    equipes_encontradas = set()
    for linha in dados_robos:
        partes = [p.strip() for p in linha.split(',')]
        robot_name = partes[1]
        equipe = robot_name.split('.')[0].replace('*', '').strip()
        # Normaliza para o nome da equipe principal
        for eq in EQUIPES:
            if equipe.lower() == eq.lower():
                equipes_encontradas.add(eq)
    for eq in equipes_encontradas:
        jogos_por_equipe[eq] += 1
        arquivos_por_equipe[eq].append(arquivo)

print('Relatório de jogos por equipe:')
for equipe, jogos in jogos_por_equipe.items():
    status = ''
    if jogos < 13:
        status = ' << MENOS de 13'
    elif jogos > 13:
        status = ' << MAIS de 13'
    print(f'{equipe}: {jogos}{status}')

# Mostra arquivos para equipes com contagem diferente de 13
for equipe, jogos in jogos_por_equipe.items():
    if jogos != 13:
        print(f'\nArquivos de jogos para {equipe} ({jogos} jogos):')
        for arq in sorted(arquivos_por_equipe[equipe]):
            print(f'  - {arq}') 

print(f"Tempo de execução: {time.time() - start_time:.2f} segundos")