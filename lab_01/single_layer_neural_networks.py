from math import fabs
import numpy as np


def boolean_function(x1, x2, x3, x4):
    return (not x1 or not x2 or not x3) and (not x2 or not x3 or x4)


def step_activation_function(net):
    return 0 if net < 0 else 1


def softsign_activation_function(net):
    out = 0.5 * (net / (1 + fabs(net) + 1))
    return 0 if out < 0 else 1


def evaluate_neural_network(input_data, weight, function_selection):
    net = 0
    for iteration in range(5):
        net = sum(weight[iteration] * input_data[iteration])
    if function_selection is True:
        return step_activation_function(net)
    else:
        return softsign_activation_function(net)


def evaluate_error(desired, actual):
    return desired - actual


'''
def boolean_values(size):
    i = 0
    result = [[]]
    variable_values = [0,1]
    for x1 in variable_values:
        for x2 in variable_values:
            for x3 in variable_values:
                for x4 in variable_values:
                    res = [x1,x2,x3,x4]
                    result[i].append(res)
                    i+=1
    return result
'''


def correct_weight(weight, function_selection):
    n = 0.3
    if function_selection is True:
        pass
    else:
        pass


def training_neural_network(function_selection):
    weight = [0, 0, 0, 0, 0]
    result = []
    variable_values = [0, 1]
    while True:
        error = 0
        for x1 in variable_values:
            for x2 in variable_values:
                for x3 in variable_values:
                    for x4 in variable_values:
                        input_data = [1, x1, x2, x3, x4]
                        desired = boolean_function(x1, x2, x3, x4)
                        actual = evaluate_neural_network(input_data, weight, function_selection)
                        result.append(actual)
                        if actual != desired:
                            error += 1
        if error == 0:
            break


if __name__ == '__main__':
    pass
