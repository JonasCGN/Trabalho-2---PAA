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

# =========================== VERSÃO RECURSIVA ===========================

# Função recursiva para calcular fatorial
def fatorial_rec(n):
    if n == 0 or n == 1:
        return 1
    return n * fatorial_rec(n - 1)

# Função recursiva para contar frequências de letras
def contar_frequencias_rec(palavra, index, freq):
    if index >= len(palavra):
        return freq
    c = palavra[index].lower()
    freq[c] += 1  
    return contar_frequencias_rec(palavra, index + 1, freq)

# Função recursiva para calcular o denominador da fórmula
def calcular_denominador_rec(freq_values, index):
    if index >= len(freq_values):
        return 1
    
    count = freq_values[index]
    fat = fatorial_rec(count)
    return fat * calcular_denominador_rec(freq_values, index + 1)

# Função principal para calcular anagramas de forma recursiva
def calcular_anagramas_recursivo(palavra):
    # Inicializa o contador de frequências e o memo para fatoriais
    freq = Counter()
    
    # Conta a frequência de cada letra
    freq = contar_frequencias_rec(palavra, 0, freq)
    
    # Calcula o numerador (fatorial do tamanho da palavra)
    numerador = fatorial_rec(len(palavra))
    
    # Calcula o denominador (produto dos fatoriais das frequências)
    denominador = calcular_denominador_rec(list(freq.values()), 0)
    
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
        res, tempo, memoria = measure_performance(calcular_anagramas_recursivo, palavra)
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