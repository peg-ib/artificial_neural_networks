from math import fabs
import itertools
import numpy as np


def boolean_function(x1, x2, x3, x4):
    return int((not x1 or not x2 or not x3) and (not x2 or not x3 or x4))


def value_table():
    result = []
    variable_values = [0, 1]
    for x1 in variable_values:
        for x2 in variable_values:
            for x3 in variable_values:
                for x4 in variable_values:
                    res = [1, x1, x2, x3, x4]
                    result.append(res)
    return result


def step_activation_function(net):
    return 0 if net < 0 else 1, net


def softsign_activation_function(net):
    out = 0.5 * (net / (1 + fabs(net) + 1))
    return 0 if out < 0 else 1, out


def evaluate_neural_network(input_data, weights, function_selection):
    net = 0
    for iteration in range(5):
        net += weights[iteration] * input_data[iteration]
    if function_selection is True:
        return step_activation_function(net)
    else:
        return softsign_activation_function(net)


def evaluate_error(desired, actual):
    return desired - actual


def correct_weight(weights, error, values, out, function_selection):
    n = 0.3
    if function_selection is True:
        for iteration in range(5):
            weights[iteration] = weights[iteration] + n * error * values[iteration]
    else:
        for iteration in range(5):
            weights[iteration] = weights[iteration] + n * error * (2 / (2 + 2 * fabs(out)) ** 2) * values[iteration]
    return weights


def learning_neural_network(function_selection):
    weights = [0, 0, 0, 0, 0]
    bool_values = value_table()
    while True:
        errors = 0
        result = []
        res = []
        for value in bool_values:
            desired = boolean_function(value[1], value[2], value[3], value[4])
            actual, out = evaluate_neural_network(value, weights, function_selection)
            res.append(desired)
            result.append(actual)
            error = evaluate_error(desired, actual)
            weights = correct_weight(weights, error, value, out, function_selection)
            if actual != desired:
                errors += 1
        print(result)
        print(errors)
        if errors == 0:
            break


# True - step_activation_function
# False - softsign_activation_function


if __name__ == '__main__':
    learning_neural_network(True)
    learning_neural_network(False)

