
#include <iostream>
#include <memory>


typedef struct Arguments {
    // User specified function.
    void (*ode)(double, double*, const unsigned long int, double*);
    // shape(N, ), 1d array.
    // User specified initial values with shape (nCols,)
    double *y;
    const unsigned long int iterations;
    const unsigned long int ncols;
    double t_0;
    const double t;
    double *t_out;
    double *y_out;
} Arguments;

void euler(Arguments *args) {
    // At every iterations, this is used to fetch the update from the
    // user specified ODE.
    std::shared_ptr<double[]> yTempShared( new double[args->ncols]);
    double *yTemp = yTempShared.get();
    const unsigned long int ncols = args->ncols;
    double t_0 = args->t_0;
    double *y = args->y;
    double *y_out = args->y_out;
    double *t_out = args->t_out;

    void (*ode)(double, double*, const unsigned long int, double*) = args->ode;
    args->t_out[0] = t_0;

    // Initialize the first values.
    for (int idx = 0; idx < ncols; ++idx) {
        y_out[idx] = y[idx];
    }

    const double step_size = (args->t - t_0) / (double) args->iterations;
    // Start iterating at 1 since we have default values for 0.
    for (unsigned long int i = 1; i <= args->iterations; i++) {
        t_0 += step_size;
        // Update yTempwith the user specified ode.
        ode(t_0, y, ncols, yTemp);
        for (int j = 0; j < ncols; j++) {
            y[j] += step_size * yTemp[j];
            y_out[i * (j + ncols)] = y[j];
        }

        t_out[i] = t_0;
    }
}



extern "C" {
    void euler_lib(Arguments *args) {
        euler(args);
    }
}