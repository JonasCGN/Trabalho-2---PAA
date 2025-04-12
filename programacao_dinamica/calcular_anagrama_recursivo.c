#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/resource.h>

#define MAX_PALAVRA 100
#define ALPHABET_SIZE 26
#define MAX_FAT 100

typedef struct {
    char *path;
    int qtd_palavras;
    int qtd_testes;
    int mostrar_resultado;
} args;

// =========================== VERSÃO RECURSIVA ===========================

long long fatorialRec(int n, long long *memo) {
    if (n == 0 || n == 1) return 1;
    if (memo[n] != 0) return memo[n];
    return memo[n] = n * fatorialRec(n - 1, memo);
}

void contarFrequenciasRec(const char *palavra, int index, int freq[]) {
    if (palavra[index] == '\0') return;
    char c = palavra[index];
    if (c >= 'A' && c <= 'Z') c += 32;
    if (c >= 'a' && c <= 'z') freq[c - 'a']++;
    contarFrequenciasRec(palavra, index + 1, freq);
}

long long calcularDivisorRec(int freq[], int index) {
    if (index == ALPHABET_SIZE) return 1;
    long long atual = 1;
    if (freq[index] > 1) atual = fatorialRec(freq[index], NULL);  // Calcula fatorial aqui
    return atual * calcularDivisorRec(freq, index + 1);
}

long long calcularAnagramasRecursivo(const char *palavra) {
    long long memo[MAX_FAT] = {0};  // Armazena resultados de fatoriais
    int freq[ALPHABET_SIZE] = {0};
    contarFrequenciasRec(palavra, 0, freq);
    int n = strlen(palavra);
    return fatorialRec(n, memo) / calcularDivisorRec(freq, 0);
}

// =========================== FUNÇÃO PARA MEDIR MEMÓRIA ===========================

long get_mem_kb() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    return usage.ru_maxrss; // em KB
}

// =========================== ARGUMENTOS E UTILITÁRIOS ===========================

void ler_args(int argc, char *argv[], args *a) {
    if (argc < 5) {
        printf("Uso: %s <arquivo.txt> <qtd_palavras> <qtd_testes> <mostrar_resultado>\n", argv[0]);
        exit(1);
    }
    a->path = argv[1];
    a->qtd_palavras = atoi(argv[2]);
    a->qtd_testes = atoi(argv[3]);
    a->mostrar_resultado = atoi(argv[4]);
    if (a->qtd_palavras <= 0 || a->qtd_testes <= 0) {
        printf("Parâmetros inválidos!\n");
        exit(1);
    }
}

void ler_palavras(char **palavras, int qtd, const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) {
        printf("Erro ao abrir arquivo: %s\n", path);
        exit(1);
    }
    for (int i = 0; i < qtd; i++) {
        palavras[i] = malloc(MAX_PALAVRA);
        if (fscanf(f, "%s", palavras[i]) != 1) {
            printf("Erro ao ler palavra %d\n", i + 1);
            exit(1);
        }
    }
    fclose(f);
}

// =========================== MAIN ===========================

int main(int argc, char *argv[]) {
    args a;
    ler_args(argc, argv, &a);

    char **palavras = malloc(a.qtd_palavras * sizeof(char *));
    ler_palavras(palavras, a.qtd_palavras, a.path);

    for (int i = 0; i < a.qtd_palavras; i++) {
        double tempo_rec = 0;
        long long res_rec = 0;
        long memoria_rec = 0;

        for (int t = 0; t < a.qtd_testes; t++) {
            // Recursiva
            long mem_before = get_mem_kb();
            clock_t inicio = clock();
            res_rec = calcularAnagramasRecursivo(palavras[i]);
            clock_t fim = clock();
            long mem_after = get_mem_kb();
            tempo_rec += (double)(fim - inicio) / CLOCKS_PER_SEC;
            memoria_rec += (mem_after - mem_before);
        }

        tempo_rec /= a.qtd_testes;
        memoria_rec /= a.qtd_testes;

        printf("Palavra: %-20s | Rec: %.6fs, %ldKB",palavras[i], tempo_rec, memoria_rec);

		printf("⚠️  Resultado divergente! Rec: %lld, Dyn: %lld\n", res_rec);

        if (a.mostrar_resultado)
            printf("Anagramas: %lld\n", res_rec);
    }

    for (int i = 0; i < a.qtd_palavras; i++)
        free(palavras[i]);
    free(palavras);

    return 0;
}
