"""
O objetivo desse script é:
1. Pegar os dados do arquivo csv
2. Somar os dados de resultados de cada batalha robocode e salvar em dois novos arquivos com a posicao final de cada equipe baseado em Chave A e Chave B
Ex: O robo Os_Fieis.Cabelinho_03 é da Equipe chamada Os Fieis , e a Equipe Os Fieis esta na Chave A
Devemos somar 5 pontos para a equipe vencedora, 
O resultado final do CSV deve ser o seguinte
POSICAO, EQUIPE, SOMA PONTOS, JOGOS, VITORIA, EMPATE, DERROTA , GP, GC, SG , % 

"""

import os
import sys
import time
import random
import requests
import json
import pandas as pd
import numpy as np

# Dicionário de equipes por chave
EQUIPES_CHAVE = {
    'A': [
        'SemNomeMasFunciona',
        'Uniao_Flasco',
        'bppd',
        'Xi_Beeu_z40',
        'Compilou_apanhou',
    ],
    'B': [
        'OS_DIGITJA_RAPDICO',
        'Os_Fuscoes',
        'Os_Fieis',
        'os_decanos',
        'CARIJOS_DA_PAMONHATRONICA',
    ]
}


EQUIPE_PARA_CHAVE = {equipe: 'A' for equipe in EQUIPES_CHAVE['A']}
EQUIPE_PARA_CHAVE.update({equipe: 'B' for equipe in EQUIPES_CHAVE['B']})

import re

def extrair_equipe(robot_name):
    return robot_name.split('.')[0].replace('*', '').strip()

estatisticas = {chave: {} for chave in ['A', 'B']}

partidas_dir = 'partidas'
for arquivo in os.listdir(partidas_dir):
    if not arquivo.endswith('.csv'):
        continue
    with open(os.path.join(partidas_dir, arquivo), 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    # Pula cabeçalhos e pega apenas as linhas dos robôs
    dados_robos = [l.strip() for l in linhas if re.match(r'^[0-9]+(st|nd|rd|th),', l.strip())]
    if not dados_robos:
        continue

    robos = []
    for linha in dados_robos:
        partes = [p.strip() for p in linha.split(',')]
        rank = partes[0]
        robot_name = partes[1]
        total_score = int(partes[2].split(' ')[0])
        equipe = extrair_equipe(robot_name)
        robos.append({
            'rank': rank,
            'equipe': equipe,
            'total_score': total_score,
            'robot_name': robot_name
        })
    equipes_partida = {}
    for r in robos:
        eq = r['equipe']
        if eq not in equipes_partida:
            equipes_partida[eq] = 0
        equipes_partida[eq] += r['total_score']
    equipes_ordenadas = sorted(equipes_partida.items(), key=lambda x: x[1], reverse=True)

    for i, (equipe, score) in enumerate(equipes_ordenadas):
        if equipe not in EQUIPE_PARA_CHAVE:
            continue  
        chave = EQUIPE_PARA_CHAVE[equipe]
        if equipe not in estatisticas[chave]:
            estatisticas[chave][equipe] = {
                'SOMA_PONTOS': 0,
                'JOGOS': 0,
                'VITORIA': 0,
                'DERROTA': 0,
                'GP': 0,
                'GC': 0,
            }
        estatisticas[chave][equipe]['JOGOS'] += 1
        estatisticas[chave][equipe]['GP'] += score
        estatisticas[chave][equipe]['GC'] += sum([s for eq, s in equipes_partida.items() if eq != equipe])
        if i == 0:
            estatisticas[chave][equipe]['SOMA_PONTOS'] += 5
            estatisticas[chave][equipe]['VITORIA'] += 1
        else:
            estatisticas[chave][equipe]['DERROTA'] += 1

# Calcula SG e %
for chave in estatisticas:
    for equipe, stats in estatisticas[chave].items():
        stats['SG'] = stats['GP'] - stats['GC']
        stats['%'] = round(100 * stats['SOMA_PONTOS'] / (stats['JOGOS'] * 5), 2) if stats['JOGOS'] > 0 else 0

# Gera CSVs de saída
import csv

def salvar_csv(chave, nome_arquivo):
    equipes_ordenadas = sorted(estatisticas[chave].items(), key=lambda x: (-x[1]['SOMA_PONTOS'], -x[1]['SG'], -x[1]['GP']))
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['POSICAO', 'EQUIPE', 'SOMA PONTOS', 'JOGOS', 'VITORIA', 'DERROTA', 'GP', 'GC', 'SG', '%'])
        for i, (equipe, stats) in enumerate(equipes_ordenadas, 1):
            writer.writerow([
                i, equipe, stats['SOMA_PONTOS'], stats['JOGOS'], stats['VITORIA'], stats['DERROTA'],
                stats['GP'], stats['GC'], stats['SG'], stats['%']
            ])

salvar_csv('A', 'resultado_chave_a.csv')
salvar_csv('B', 'resultado_chave_b.csv')