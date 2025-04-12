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

// =========================== VERSÃO DINÂMICA ===========================

void calcularFatoriais(long long *fatorial, int n) {
    fatorial[0] = 1;
    for (int i = 1; i <= n; i++) {
        fatorial[i] = fatorial[i - 1] * i;
    }
}

long long calcularAnagramasDinamico(const char *palavra) {
    int freq[ALPHABET_SIZE] = {0};
    int n = strlen(palavra);
    long long fatorial[MAX_FAT];
    calcularFatoriais(fatorial, n);

    for (int i = 0; i < n; i++) {
        char c = palavra[i];
        if (c >= 'A' && c <= 'Z') c += 32;
        if (c >= 'a' && c <= 'z') freq[c - 'a']++;
    }

    long long resultado = fatorial[n];
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (freq[i] > 1) resultado /= fatorial[freq[i]];
    }

    return resultado;
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
        buffer[strcspn(buffer, "\n")] = '\0';  // Remove o '\n' do final
        palavras[count] = malloc(strlen(buffer) + 1);
        strcpy(palavras[count], buffer);
        count++;
    }

    fclose(f);

    if (count < qtd) {
        printf("⚠️  Aviso: arquivo contém apenas %d palavras, mas %d foram solicitadas.\n", count, qtd);
    }
}

void mostrar_palavras(char **palavras,int qtd){
    for(int i=0;i<qtd;i++){
        printf("%d - %s\n",i,palavras[i]);
    }
}

int main(int argc, char *argv[]) {
    args a;
    ler_args(argc, argv, &a);

    char **palavras = malloc(a.qtd_palavras * sizeof(char *));
    ler_palavras(palavras, a.qtd_palavras, a.path);
    // mostrar_palavras(palavras,a.qtd_palavras);

    double tempo_dyn = 0;
    long long res_dyn = 0;
    long memoria_dyn = 0;

    for (int i = 0; i < a.qtd_palavras; i++) {
        

        for (int t = 0; t < a.qtd_testes; t++) {
            long mem_before = get_mem_kb();
            clock_t inicio = clock();
            res_dyn = calcularAnagramasDinamico(palavras[i]);
            clock_t fim = clock();
            long mem_after = get_mem_kb();
            tempo_dyn += (double)(fim - inicio) / CLOCKS_PER_SEC;
            memoria_dyn += (mem_after - mem_before);
        }
        
        if (a.mostrar_resultado)
            printf("Palavra: %-20s | Rec: %.6fs, %ldKB |  Resultado: %lld\n", palavras[i], tempo_dyn, memoria_dyn, res_dyn);
    }
    
    tempo_dyn /= a.qtd_testes;
    memoria_dyn /= a.qtd_testes;

    printf("Tempo:%.6fs Memoria:%ldKB\n",tempo_dyn, memoria_dyn);

    for (int i = 0; i < a.qtd_palavras; i++)
        free(palavras[i]);
    free(palavras);

    return 0;
}