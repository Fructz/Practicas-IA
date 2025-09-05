#include <stdio.h>
#define MAX 4

int max(int a, int b) {
    return (a > b) ? a : b;
}

int main() {
    int personas[MAX];
    int aux, tiempoTotal = 0;

    for (int i = 0; i < MAX; i++) {
        printf("Tiempo persona %d: ", i + 1);
        scanf("%d", &personas[i]);
    }

    for (int i = 0; i < MAX - 1; i++) {
        for (int j = 0; j < MAX - 1 - i; j++) {
            if (personas[j] > personas[j + 1]) {
                aux = personas[j];
                personas[j] = personas[j + 1];
                personas[j + 1] = aux;
            }
        }
    }

    int A = personas[0]; // más rápido
    int B = personas[1]; // segundo más rápido
    int C = personas[2]; // segundo más lento
    int D = personas[3]; // más lento

    // Movimiento 1: cruzan A y B
    tiempoTotal += max(A, B);
    printf("Cruzan %d y %d -> Tiempo acumulado: %d\n", A, B, tiempoTotal);

    // Movimiento 2: regresa A
    tiempoTotal += A;
    printf("Regresa %d -> Tiempo acumulado: %d\n", A, tiempoTotal);

    // Movimiento 3: cruzan C y D
    tiempoTotal += max(C, D);
    printf("Cruzan %d y %d -> Tiempo acumulado: %d\n", C, D, tiempoTotal);

    // Movimiento 4: regresa B
    tiempoTotal += B;
    printf("Regresa %d -> Tiempo acumulado: %d\n", B, tiempoTotal);

    // Movimiento 5: cruzan A y B
    tiempoTotal += max(A, B);
    printf("Cruzan %d y %d -> Tiempo acumulado: %d\n", A, B, tiempoTotal);

    printf("\nTiempo total mínimo: %d\n", tiempoTotal);

    return 0;
}