/*
 * Some function for getting correlation in faster way than python native.
 */

int cor(int r, double* x, int n) {
    int result = 0;
    int i, j;
    double dx;
    i = n;
    while (i-- > 0) {
        j = i;
        while (j-- > 0) {
            dx = x[i] - x[j];
            if (r > fabs(dx)) {
                result ++;
            }
        }
    }
    return result * 2;
}

int cor2(int r, double* x, double* y, int n) {
    int result = 0;
    int i, j;
    double dx, dy;
    i = n;
    while (i-- > 0) {
        j = i;
        while (j-- > 0) {
            dx = (x[i] - x[j]);
            dy = (y[i] - y[j]);
            if (r > sqrt(dx*dx + dy*dy)) {
                result ++;
            }
        }
    }
    return result * 2;
}

int cor3(int r, double* x, double* y, double* z, int n) {
    int result = 0;
    int i, j;
    double dx, dy, dz;
    i = n;
    while (i-- > 0) {
        j = i;
        while (j-- > 0) {
            dx = (x[i] - x[j]);
            dy = (y[i] - y[j]);
            if (r > sqrt(dx*dx + dy*dy + dz*dz)) {
                result ++;
            }
        }
    }
    return result * 2;
}
