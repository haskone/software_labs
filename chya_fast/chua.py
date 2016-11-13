#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from _cor import ffi, lib

ALPHA = 7.5
BETA = 14.28
m0 = -3/7
m1 = 4/7
dt = 0.01


def f(x):
    return 0.5 * (m0 - m1) * (np.abs(x + 1) - np.abs(x - 1))


def chua(x, y, z):
    d_x = ALPHA * (-1 * m1 * x + y - f(x))
    d_y = x - y + z
    d_z = -1 * BETA * y
    return [x + d_x * dt, y + d_y * dt, z + d_z * dt]


def volume_theory(x, t):
    c = m1 if np.abs(x) > 1 else m0
    return np.exp((-1 * m1 + c + 1) * t)


def split_by_dimensions(arr):
    xs = []
    ys = []
    zs = []
    for i in arr:
        xs.append(i[0])
        ys.append(i[1])
        zs.append(i[2])
    return xs, ys, zs


def show3d(xs, ys, zs):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(xs, ys, zs)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def show2d(xs, ys):
    plt.plot(xs, ys)
    plt.show()


def show(ys):
    plt.plot(range(len(ys)), ys)
    plt.show()


def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size // 2:]


def generate_three_seq(N, tau, Y):
    tau_0 = []
    tau_1 = []
    tau_2 = []
    for m in range(N):
        tau_0.append(Y[m])
        tau_1.append(Y[m + tau])
        tau_2.append(Y[m + 2 * tau])
    return tau_0, tau_1, tau_2


if __name__ == '__main__':
    vals = []
    curr = [2., -1., 0.]
    N_max = 6000
    for _ in np.arange(1, N_max, 1):
        vals.append(curr)
        curr = chua(*curr)

    T_ini = 2900

    # getting Xs
    T_arr = split_by_dimensions(vals[T_ini:-1])[0]
    N_max -= T_ini

    # look at the autocorr plot (first local minimun)
    Tau = 130

    N = N_max - 2 * Tau - 123
    G_Y1, G_Y2, G_Y3 = generate_three_seq(N = N, tau = Tau, Y = T_arr)

    c_arr = []
    r_arr = []
    for r in range(1, 6):
        c_arr.append(np.log(lib.cor(r, G_Y1, N)))
        r_arr.append(np.log(r))

    dim_arr = []
    c_0, r_0 = 0, 0
    for c, r in zip(c_arr, r_arr):
        if r > 0:
            dim_arr.append((c - c_0)/(r - r_0))
        c_0 = c
        r_0 = r

    # result
    show(split_by_dimensions(vals[0:-1])[0])
    show(T_arr)
    show(autocorr(T_arr))

    # resurrected attractor
    show3d(G_Y1, G_Y2, G_Y3)

    # log C (log r)
    show2d(r_arr, c_arr)
    print(np.mean(dim_arr))
