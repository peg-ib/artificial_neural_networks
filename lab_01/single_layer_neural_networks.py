from math import fabs
import numpy as np


def boolean_function(x1, x2, x3, x4):
    return (not x1 or not x2 or not x3) and (not x2 or not x3 or x4)


def step_activation_function(net):  # net - сумма входных сигналов нейронов умноженная на веса.
    return 0 if net < 0 else 1


def softsign_activation_function(out):
    return 0.5 * (out / (1 + fabs(out)) + 1)


if __name__ == '__main__':
    pass
