#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define ALPHA 0.5
#define NITER 100
#define STEP 0.1

typedef struct Solution
{
    double x;
    double y;
    double value;
} Solution;

// Search domain: -5 <= x,y <= 5
int x_min = -5, x_max = 5, y_min = -5, y_max = 5;

Solution insertSol(double, double);
double himmelblau(double, double);
void simAnnealing(Solution *, Solution *, double, double);

int main() {
    srand(time(NULL));

    double t_min = 0.001, T = 10;

    // Generate a random point within [-5,5], as this is the search domain. This will be our initial solution.
    double x = x_min + (rand() / (double)RAND_MAX) * (x_max - x_min);
    double y = y_min + (rand() / (double)RAND_MAX) * (y_max - y_min);
    Solution sol = insertSol(x, y);

    Solution current = sol;
    Solution best = sol;
    Solution neighbor;
    double Delta, P, u;

    simAnnealing(&current, &best, T, t_min);

    printf("Best found solution:\n");
    printf("x = %f, y = %f, f(x,y) = %f\n", best.x, best.y, best.value);

    return 0;
}

void simAnnealing(Solution *current, Solution *best, double T, double t_min){
    Solution neighbor;
    double Delta, P, u;

    FILE *fp = fopen("data.csv", "w");
    if (!fp) {
        printf("Error al crear archivo\n");
        return;
    }

    fprintf(fp, "x,y,value\n");

    while (T > t_min) {
        for (int i = 0; i < NITER; i++) {
            double delta_x = -STEP + (rand() / (double)RAND_MAX) * (2 * STEP);
            double delta_y = -STEP + (rand() / (double)RAND_MAX) * (2 * STEP);

            // Calcular vecino
            double x_nei = current->x + delta_x;
            double y_nei = current->y + delta_y;

            // Aplicar límites
            if (x_nei < x_min) x_nei = x_min;
            if (x_nei > x_max) x_nei = x_max;
            if (y_nei < y_min) y_nei = y_min;
            if (y_nei > y_max) y_nei = y_max;

            neighbor = insertSol(x_nei, y_nei);

            // Calcular Δ
            Delta = neighbor.value - current->value;

            if (Delta <= 0) {
                *current = neighbor;
            } else {
                P = exp(-Delta / T);
                u = rand() / (double)RAND_MAX;
                if (u < P)
                    *current = neighbor;
            }

            // Actualizar mejor solución
            if (current->value < best->value) *best = *current;
            fprintf(fp, "%f,%f,%f\n", current->x, current->y, current->value);
        }

        // Enfriar
        T = ALPHA * T;
    }
    fclose(fp);
}

double himmelblau(double x, double y) {
    // Function : f(x,y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2
    double p1 = pow(x, 2) + y - 11;
    double p2 = x + pow(y, 2) - 7;
    return pow(p1, 2) + pow(p2, 2);
}

Solution insertSol(double x, double y) {
    Solution sol;
    sol.x = x;
    sol.y = y;
    sol.value = himmelblau(x, y);
    return sol;
}