import sys
import time
import tracemalloc
import gc
from collections import Counter

class Args:
    def __init__(self, path, qtd_testes, mostrar_resultado):
        self.path = path
        self.qtd_testes = qtd_testes
        self.mostrar_resultado = mostrar_resultado

# =========================== VERSÃO ITERATIVA ===========================

# Função iterativa para calcular fatorial
def fatorial_iter(n):
    resultado = 1
    for i in range(2, n+1):
        resultado *= i
    return resultado

# Função iterativa para contar frequências de letras
def contar_frequencias_iter(palavra):
    freq = Counter()
    for c in palavra:
        freq[c.lower()] += 1
    return freq

# Função iterativa para calcular o denominador da fórmula
def calcular_denominador_iter(freq_values):
    denominador = 1
    for count in freq_values:
        if count > 1:  # Otimização: não precisamos calcular fatorial de 1
            denominador *= fatorial_iter(count)
    return denominador

# Função principal para calcular anagramas de forma iterativa
def calcular_anagramas_iterativo(palavra):
    # Inicializa o contador de frequências
    freq = contar_frequencias_iter(palavra)
    
    # Calcula o numerador (fatorial do tamanho da palavra)
    numerador = fatorial_iter(len(palavra))
    
    # Calcula o denominador (produto dos fatoriais das frequências)
    denominador = calcular_denominador_iter(freq.values())
    
    # Retorna o resultado da fórmula
    return numerador // denominador

# =========================== FUNÇÃO PARA MEDIR MEMÓRIA E TEMPO ===========================

def measure_performance(func, *args):
    gc.collect()  # Força coleta de lixo antes da medição
    
    # Mede tempo
    inicio = time.time()
    
    # Mede memória
    tracemalloc.start()
    result = func(*args)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Calcula tempo
    fim = time.time()
    tempo = fim - inicio
    
    return result, tempo, peak / 1024  # Resultado, tempo em segundos, memória em KB

# =========================== ARGUMENTOS E UTILITÁRIOS ===========================

def ler_args(argc, argv):
    if argc < 4:
        print(f"Uso: {argv[0]} <arquivo.txt> <qtd_testes> <mostrar_resultado>")
        sys.exit(1)
    
    path = argv[1]
    qtd_testes = int(argv[2])
    mostrar_resultado = int(argv[3])
    return Args(path, qtd_testes, mostrar_resultado)

def ler_palavra(path):
    try:
        with open(path, 'r') as f:
            palavra = f.readline().strip()
            return palavra
    except FileNotFoundError:
        print(f"Erro: arquivo {path} não encontrado.")
        sys.exit(1)

# =========================== MAIN ===========================

def main():
    args = ler_args(len(sys.argv), sys.argv)
    palavra = ler_palavra(args.path)
    
    tempo_total = 0
    memoria_total = 0
    resultado = None
    
    for i in range(args.qtd_testes):
        res, tempo, memoria = measure_performance(calcular_anagramas_iterativo, palavra)
        tempo_total += tempo
        memoria_total += memoria
        resultado = res
    
    tempo_medio = tempo_total / args.qtd_testes
    memoria_media = memoria_total / args.qtd_testes
    
    if args.mostrar_resultado:
        print(f"Palavra: {palavra}")
        print(f"Quantidade de anagramas: {resultado}")
        print(f"Tempo médio: {tempo_medio:.6f}s")
        print(f"Memória média: {memoria_media:.2f} KB")
    
    print(f"Tempo:{tempo_medio:.6f}s Memoria:{memoria_media:.2f}KB QTD:{len(palavra)}")

if __name__ == "__main__":
    main()