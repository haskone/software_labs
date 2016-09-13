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


def gen_plots(seq_a, seq_b_x, seq_c_x):
    plt.plot(np.arange(len(seq_a)), seq_a, 'r--',
             np.arange(len(seq_b)), seq_b_x, 'bs',
             np.arange(len(seq_c)), seq_c_x, 'g^')
    plt.show()


def make_it_bin(seq, border=0.5):
    return [1 if item > border else
            0 for item in seq]


def gen_seqs():
    seq_a = gen_seq(0.001, gen_a, 100)
    seq_b = gen_seq((0.01, 0.1), gen_b, 100)
    seq_c = gen_seq((0.01, 0.1), gen_c, 100)

    return seq_a, seq_b, seq_c

if __name__ == '__main__':
    seq_a, seq_b, seq_c = gen_seqs()
    print('a: ', seq_a)
    print('b: ', seq_b)
    print('c: ', seq_c)

    seq_b_x = [t[0] for t in seq_b]
    seq_c_x = [t[0] for t in seq_c]
    print('bin a: ', make_it_bin(seq_a))
    print('bin b: ', make_it_bin(seq_b_x))
    print('bin c: ', make_it_bin(seq_c_x))

    gen_plots(seq_a, seq_b_x, seq_c_x)
