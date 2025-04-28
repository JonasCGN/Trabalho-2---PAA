import sys
import time
import psutil  # For memory measurement
import gc  # For garbage collection
import tracemalloc  # For memory tracking

MAX_PALAVRA = 100
ALPHABET_SIZE = 26
MAX_FAT = 100

class Args:
    def __init__(self, path, qtd_palavras, qtd_testes, mostrar_resultado):
        self.path = path
        self.qtd_palavras = qtd_palavras
        self.qtd_testes = qtd_testes
        self.mostrar_resultado = mostrar_resultado

# =========================== VERSÃO DINÂMICA ===========================

def calcular_fatoriais(n):
    fatorial = [0] * MAX_FAT
    fatorial[0] = 1
    for i in range(1, n + 1):
        fatorial[i] = fatorial[i - 1] * i
    return fatorial

def calcular_anagramas_dinamico(palavra):
    freq = [0] * ALPHABET_SIZE
    n = len(palavra)
    fatorial = calcular_fatoriais(n)
    
    for c in palavra:
        if 'A' <= c <= 'Z':
            c = chr(ord(c) + 32)  # Convert to lowercase
        if 'a' <= c <= 'z':
            freq[ord(c) - ord('a')] += 1
    
    resultado = fatorial[n]
    for i in range(ALPHABET_SIZE):
        if freq[i] > 1:
            resultado //= fatorial[freq[i]]
    
    return resultado

# =========================== FUNÇÃO PARA MEDIR MEMÓRIA ===========================

def measure_memory_usage(func, *args, **kwargs):
    """Measure memory used by a function"""
    gc.collect()  # Force garbage collection before measurement
    tracemalloc.start()
    result = func(*args, **kwargs)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # Return result and memory usage in KB
    return result, peak / 1024

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

def mostrar_palavras(palavras):
    for i, palavra in enumerate(palavras):
        print(f"{i} - {palavra}")

# =========================== MAIN ===========================

def main():
    a = ler_args(len(sys.argv), sys.argv)
    
    palavras = ler_palavras(a.qtd_palavras, a.path)
    # mostrar_palavras(palavras)
    
    tempo_dyn = 0
    res_dyn = 0
    memoria_dyn = 0
    
    for i in range(len(palavras)):
        tempo_palavra = 0
        memoria_palavra = 0
        
        for t in range(a.qtd_testes):
            inicio = time.time()
            res_dyn, mem_usage = measure_memory_usage(calcular_anagramas_dinamico, palavras[i])
            fim = time.time()
            
            tempo_palavra += (fim - inicio)
            memoria_palavra += mem_usage
        
        tempo_palavra /= a.qtd_testes
        memoria_palavra /= a.qtd_testes
        tempo_dyn += tempo_palavra
        memoria_dyn += memoria_palavra
        
        if a.mostrar_resultado:
            print(f"Palavra: {palavras[i]:<20} | Dyn: {tempo_palavra:.6f}s, {memoria_palavra:.2f}KB | Resultado: {res_dyn}")
    
    tempo_dyn /= len(palavras)
    memoria_dyn /= len(palavras)
    
    print(f"Tempo:{tempo_dyn:.6f}s Memoria:{memoria_dyn:.2f}KB Qtd:{len(palavras)}")

if __name__ == "__main__":
    main()