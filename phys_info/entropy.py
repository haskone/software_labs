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


def make_it_bin(seq, border=0.5):
    return [1 if item > border else
            0 for item in seq]


def gen_sub_seq_item(v, n, seq):
    s_n = 0
    for v_index in range(1, v + 1):
        s_n += np.power(2, v - v_index) * seq[v_index * n - v_index + 1]
    return s_n


def gen_sub_seq(seq_bin, v_seq):
    v_map = {}
    for v in v_seq:
        n_seq = range(1, round(len(seq_bin) / v))
        seq_a_sub = []
        for n in n_seq:
            seq_a_sub.append(gen_sub_seq_item(v, n, seq_bin))
        v_map[v] = seq_a_sub
    return v_map


def get_prob(sub_seq):
    prob_v_map = {}
    for v, seq in sub_seq.items():
        prob_map = {}
        l_seq = len(seq)
        for item in set(seq):
            prob_map[item] = seq.count(item) / l_seq
        prob_v_map[v] = prob_map
    return prob_v_map


def get_shannon(probs_map):
    res = 0
    for item in probs_map.values():
        res += item * np.log2(item)
    return -1 * res


def get_renyi(probs_map, b):
    res = 0
    for item in probs_map.values():
        res += np.power(item, b)
    return -1 * np.log2(res) * (1 / (b - 1))


def gen_plots(seqs, labels):
    lines = []
    for plot in zip(seqs, labels):
        line, = plt.plot(np.arange(len(plot[0])), plot[0], label=plot[1])
        lines.append(line)
    plt.legend(lines, labels, bbox_to_anchor=(1, 0.5))
    plt.show()


if __name__ == '__main__':

    seq_chose = gen_seq(0.5, gen_a, 10000)
    seq_bin = make_it_bin(seq_chose)
    seq_sub = gen_sub_seq(seq_bin, v_seq=range(2, 21))
    probs_map = get_prob(seq_sub)

    entropy_set = []
    renyi_full_2 = []
    for prob in probs_map.values():
        renyi_full_2.append(get_renyi(prob, 2))
    entropy_set.append(renyi_full_2)

    renyi_full_3 = []
    for prob in probs_map.values():
        renyi_full_3.append(get_renyi(prob, 3))
    entropy_set.append(renyi_full_3)

    shannon_full = []
    for prob in probs_map.values():
        shannon_full.append(get_shannon(prob))
    entropy_set.append(shannon_full)

    gen_plots(entropy_set, ['renyi_2', 'renyi_3', 'shannon'])
