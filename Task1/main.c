#include <math.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define Block_sz 64
#define EPS 0.1
#define N 300
static int min(int a, int b) { return a < b ? a : b; }

double **create_array()
{
    double **res = calloc(N + 2, sizeof(*res));
    for (int i = 0; i < N + 2; i++)
        res[i] = calloc(N + 2, sizeof(*res[i]));
    return res;
}

void free_array(double **arr)
{
    for (int i = 0; i < N + 2; i++)
    {
        free(arr[i]);
    }
    return free(arr);
}

int main()
{
    int threads[] = {1, 2, 4, 6, 8, 12};

    int NB = (N - 2) / 64;

    if (64 * NB != N - 2)
        NB += 1;
    double h = 1.0 / (N + 1);
    printf("Size: %d\n", N);

    for (int num_thr = 0; num_thr < 6; num_thr++)
    {

        int counter = 0;
        double dmax = 0;
        double **u = create_array();
        double *dm = calloc(NB, sizeof(*dm));

        double **f = create_array();

        for (int i = 0; i < N + 2; i++)
        {
            for (int j = 0; j < N + 2; j++)
            {
                double x = i * h;
                double y = j * h;
                if ((i == N + 1) || (i == 0) || (j == 0) || (j == N + 1))
                    u[i][j] = 500 * pow(x, 4) + 750 * pow(x, 3) + 210 * pow(y, 2) + x * y + 2000;
                else
                    u[i][j] = 0;
                f[i][j] = 6000 * pow(x, 2) + 4500 * x + 422;
            }
        }
        double t1 = omp_get_wtime();
        omp_set_num_threads(threads[num_thr]);
        do
        {
            counter++;

            dmax = 0;
            for (int nx = 0; nx < NB; nx++)
            {
                dm[nx] = 0;
#pragma omp parallel for shared(nx)
                for (int i = 0; i < nx + 1; i++)
                {
                    int j = nx - i;

                    int i0 = 1 + i * Block_sz;
                    int im = min(i0 + Block_sz, N + 1);
                    int j0 = 1 + j * Block_sz;
                    int jm = min(j0 + Block_sz, N + 1);
                    double dm1 = 0;
                    for (int i = i0; i < im; i++)
                    {
                        for (int j = j0; j < jm; j++)
                        {

                            double temp = u[i][j];
                            u[i][j] = 0.25 * (u[i - 1][j] + u[i + 1][j] +
                                              u[i][j - 1] + u[i][j + 1] - h * h * f[i][j]);
                            double d = fabs(temp - u[i][j]);
                            if (dm1 < d)
                                dm1 = d;
                        }
                    }
                    if (dm[i] < dm1)
                        dm[i] = dm1;
                }
            }

            for (int nx = NB - 2; nx > -1; nx--)
            {
#pragma omp parallel for shared(nx)
                for (int i = NB - nx - 1; i < NB; i++)
                {
                    int j = 2 * (NB - 1) - nx - i;
                    int i0 = 1 + i * Block_sz;
                    int im = min(i0 + Block_sz, N + 1);
                    int j0 = 1 + j * Block_sz;
                    int jm = min(j0 + Block_sz, N + 1);
                    double dm1 = 0;
                    for (int i = i0; i < im; i++)
                    {
                        for (int j = j0; j < jm; j++)
                        {

                            double temp = u[i][j];
                            u[i][j] = 0.25 * (u[i - 1][j] + u[i + 1][j] +
                                              u[i][j - 1] + u[i][j + 1] - h * h * f[i][j]);
                            double d = fabs(temp - u[i][j]);
                            if (dm1 < d)
                                dm1 = d;
                        }
                    }
                    if (dm[i] < dm1)
                        dm[i] = dm1;
                }
            }
            for (int i = 0; i < NB; i++)
            {
                if (dmax < dm[i])
                    dmax = dm[i];
            }

        } while (dmax > EPS);

        double t2 = omp_get_wtime();
        free_array(u);
        free(dm);
        free_array(f);
        printf("Count: %d, threads: %d, time execution: %.2f second\n", counter, threads[num_thr], t2 - t1);
    }

    return 0;
}