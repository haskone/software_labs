#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

MU = 3.8
ALPHA = 1.4
BETA = 0.3


def gen_a(x):
    return MU * x * (1 - x)


def gen_b(x, y):
    return 1 - ALPHA * x * x + y, BETA * x


def gen_c(x, y):
    return 1 - ALPHA * np.absolute(x) + y, BETA * x


def gen_seq(start, func, length):
    curr = start
    seq = [curr, ]
    for i in range(length):
        if isinstance(curr, tuple):
            curr = func(curr[0], curr[1])
        else:
            curr = func(curr)
        seq.append(curr)
    return seq


def gen_plots():
    seq_a = gen_seq(0.001, gen_a, 100)
    seq_b = gen_seq((0.01, 0.01), gen_b, 100)
    seq_c = gen_seq((0.01, 0.01), gen_c, 100)

    print(seq_a)
    plt.plot(np.arange(len(seq_a)), seq_a, 'r--')
    plt.show()

gen_plots()
