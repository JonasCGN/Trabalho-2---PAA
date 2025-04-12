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
    if (memo && memo[n] != 0) return memo[n];  // proteção contra ponteiro NULL
    long long resultado = n * fatorialRec(n - 1, memo);
    if (memo) memo[n] = resultado;
    return resultado;
}

void contarFrequenciasRec(const char *palavra, int index, int freq[]) {
    if (palavra[index] == '\0') return;
    char c = palavra[index];
    if (c >= 'A' && c <= 'Z') c += 32;
    if (c >= 'a' && c <= 'z') freq[c - 'a']++;
    contarFrequenciasRec(palavra, index + 1, freq);
}

long long calcularDivisorRec(int freq[], int index, long long *memo) {
    if (index == ALPHABET_SIZE) return 1;
    long long atual = 1;
    if (freq[index] > 1) atual = fatorialRec(freq[index], memo);
    return atual * calcularDivisorRec(freq, index + 1, memo);
}

long long calcularAnagramasRecursivo(const char *palavra) {
    long long memo[MAX_FAT] = {0};
    int freq[ALPHABET_SIZE] = {0};
    contarFrequenciasRec(palavra, 0, freq);
    int n = strlen(palavra);
    return fatorialRec(n, memo) / calcularDivisorRec(freq, 0, memo);
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
        perror("Erro ao abrir o arquivo");
        exit(1);
    }

    char buffer[MAX_PALAVRA];
    int count = 0;

    while (fgets(buffer, sizeof(buffer), f) && count < qtd) {
        buffer[strcspn(buffer, "\n")] = '\0';
        palavras[count] = malloc(strlen(buffer) + 1);
        strcpy(palavras[count], buffer);
        count++;
    }

    fclose(f);

    if (count < qtd) {
        printf("⚠️  Aviso: arquivo contém apenas %d palavras, mas %d foram solicitadas.\n", count, qtd);
    }
}

// =========================== MAIN ===========================

int main(int argc, char *argv[]) {
    args a;
    ler_args(argc, argv, &a);

    char **palavras = malloc(a.qtd_palavras * sizeof(char *));
    ler_palavras(palavras, a.qtd_palavras, a.path);
    double tempo_rec = 0;
    long long res_rec = 0;
    long memoria_rec = 0;

    for (int i = 0; i < a.qtd_palavras; i++) {
        

        for (int t = 0; t < a.qtd_testes; t++) {
            long mem_before = get_mem_kb();
            clock_t inicio = clock();
            res_rec = calcularAnagramasRecursivo(palavras[i]);
            clock_t fim = clock();
            long mem_after = get_mem_kb();
            tempo_rec += (double)(fim - inicio) / CLOCKS_PER_SEC;
            memoria_rec += (mem_after - mem_before);
        }

        if (a.mostrar_resultado)
            printf("Palavra: %-20s | Rec: %.6fs, %ldKB | Resultado: %lld\n", palavras[i], tempo_rec, memoria_rec,res_rec);
    }
    
    tempo_rec /= a.qtd_testes;
    memoria_rec /= a.qtd_testes;

    printf("Tempo:%.6fs Memoria:%ldKB\n",tempo_rec, memoria_rec);

    for (int i = 0; i < a.qtd_palavras; i++)
        free(palavras[i]);
    free(palavras);

    return 0;
}
