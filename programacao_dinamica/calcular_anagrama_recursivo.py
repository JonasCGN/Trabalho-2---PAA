import sys
import time
import tracemalloc  # Use tracemalloc instead of resource/psutil
import psutil  # Added psutil for better memory measurement

MAX_PALAVRA = 100
ALPHABET_SIZE = 26
MAX_FAT = 100

class Args:
    def __init__(self, path, qtd_palavras, qtd_testes, mostrar_resultado):
        self.path = path
        self.qtd_palavras = qtd_palavras
        self.qtd_testes = qtd_testes
        self.mostrar_resultado = mostrar_resultado

# =========================== VERSÃO RECURSIVA ===========================

def fatorial_rec(n, memo=None):
    if memo is None:
        memo = {}
    if n == 0 or n == 1:
        return 1
    if n in memo:
        return memo[n]
    resultado = n * fatorial_rec(n - 1, memo)
    memo[n] = resultado
    return resultado

def contar_frequencias_rec(palavra, index, freq):
    if index >= len(palavra):
        return
    c = palavra[index]
    if 'A' <= c <= 'Z':
        c = chr(ord(c) + 32)  # Convert to lowercase
    if 'a' <= c <= 'z':
        freq[ord(c) - ord('a')] += 1
    contar_frequencias_rec(palavra, index + 1, freq)

def calcular_divisor_rec(freq, index, memo=None):
    if memo is None:
        memo = {}
    if index == ALPHABET_SIZE:
        return 1
    atual = 1
    if freq[index] > 1:
        atual = fatorial_rec(freq[index], memo)
    return atual * calcular_divisor_rec(freq, index + 1, memo)

def calcular_anagramas_recursivo(palavra):
    memo = {}
    freq = [0] * ALPHABET_SIZE
    contar_frequencias_rec(palavra, 0, freq)
    n = len(palavra)
    return fatorial_rec(n, memo) // calcular_divisor_rec(freq, 0, memo)

# =========================== FUNÇÃO PARA MEDIR MEMÓRIA ===========================

def measure_memory(func, *args):
    tracemalloc.start()
    result = func(*args)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak / 1024  # Convert to KB

# =========================== ARGUMENTOS E UTILITÁRIOS ===========================

def ler_args(argc, argv):
    if argc < 5:
        print(f"Uso: {argv[0]} <arquivo.txt> <qtd_palavras> <qtd_testes> <mostrar_resultado>")
        sys.exit(1)
    
    path = argv[1]
    qtd_palavras = int(argv[2])
    qtd_testes = int(argv[3])
    mostrar_resultado = int(argv[4])
    
    if qtd_palavras <= 0 or qtd_testes <= 0:
        print("Parâmetros inválidos!")
        sys.exit(1)
    
    return Args(path, qtd_palavras, qtd_testes, mostrar_resultado)

def ler_palavras(qtd, path):
    try:
        with open(path, 'r') as f:
            palavras = []
            for _ in range(qtd):
                linha = f.readline().strip()
                if not linha:
                    break
                palavras.append(linha)
            
            if len(palavras) < qtd:
                print(f"⚠️  Aviso: arquivo contém apenas {len(palavras)} palavras, mas {qtd} foram solicitadas.")
            
            return palavras
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {e}")
        sys.exit(1)

# =========================== MAIN ===========================

def main():
    a = ler_args(len(sys.argv), sys.argv)
    
    palavras = ler_palavras(a.qtd_palavras, a.path)
    tempo_rec = 0
    res_rec = 0
    memoria_rec = 0
    
    for i in range(len(palavras)):
        tempo_palavra = 0
        memoria_palavra = 0
        
        for t in range(a.qtd_testes):
            inicio = time.time()
            res_rec, mem_used = measure_memory(calcular_anagramas_recursivo, palavras[i])
            fim = time.time()
            
            tempo_palavra += (fim - inicio)
            memoria_palavra += mem_used
        
        tempo_palavra /= a.qtd_testes
        memoria_palavra /= a.qtd_testes
        tempo_rec += tempo_palavra
        memoria_rec += memoria_palavra
        
        if a.mostrar_resultado:
            print(f"Palavra: {palavras[i]:<20} | Rec: {tempo_palavra:.6f}s, {memoria_palavra:.2f}KB | Resultado: {res_rec}")
    
    tempo_rec /= len(palavras)
    memoria_rec /= len(palavras)
    
    print(f"Tempo:{tempo_rec:.6f}s Memoria:{memoria_rec:.2f}KB")

if __name__ == "__main__":
    main()