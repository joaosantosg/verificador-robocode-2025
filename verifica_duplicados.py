import os
import hashlib

partidas_dir = 'partidas'
arquivos = [f for f in os.listdir(partidas_dir) if f.endswith('.csv')]
hashes = {}

for arquivo in arquivos:
    caminho = os.path.join(partidas_dir, arquivo)
    with open(caminho, 'rb') as f:
        conteudo = f.read()
        hash_arquivo = hashlib.md5(conteudo).hexdigest()
        if hash_arquivo not in hashes:
            hashes[hash_arquivo] = []
        hashes[hash_arquivo].append(arquivo)

print('Arquivos duplicados (mesmo conteúdo):')
encontrou = False
for arquivos_iguais in hashes.values():
    if len(arquivos_iguais) > 1:
        encontrou = True
        print(' - ' + ', '.join(sorted(arquivos_iguais)))
if not encontrou:
    print('Nenhum arquivo duplicado encontrado.') 