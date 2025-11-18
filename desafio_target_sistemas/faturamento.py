import json

caminho_arquivo = './dados.json'

with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

soma = 0

for i in dados:
    soma += i['valor']

faturamento = {
    "SP": 67836.43,
    "RJ": 36678.66,
    "MG": 29229.88,
    "ES": 27165.48,
    "Outros": 19849.53
}

faturamentoPorEstado = {}

for i in faturamento:
    faturamentoPorEstado[i] = (faturamento[i] / soma) * 100

print(faturamentoPorEstado)


