import itertools
from prettytable import PrettyTable
import matplotlib.pyplot as plt


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


def computation_out(net):
    return (net / (1 + abs(net)) + 1) / 2


def softsign_activation_function(net):
    out = computation_out(net)
    return 0 if out < 0.5 else 1, net


def evaluate_neural_network(input_data, weights, function_selection):
    net = 0
    for iteration in range(5):
        net += weights[iteration] * input_data[iteration]
    if function_selection == 'step':
        return step_activation_function(net)
    else:
        return softsign_activation_function(net)


def correct_weights(values, error, weights, net, function_selection):
    n = 0.3
    if function_selection == 'step':
        for iteration in range(5):
            weights[iteration] = weights[iteration] + n * error * values[iteration]
    else:
        for iteration in range(5):
            weights[iteration] = weights[iteration] + n * error * (1 / (2 * ((abs(net) + 1) ** 2))) * values[iteration]
    return weights


def actual_boolean_vector(boolean_variable_sets, weights, function_selection):
    result = []
    for value in boolean_variable_sets:
        y, net = evaluate_neural_network(value, weights, function_selection)
        result.append(y)
    return result


def desired_boolean_vector(boolean_variable_sets):
    result = []
    for value in boolean_variable_sets:
        t = boolean_function(value[1], value[2], value[3], value[4])
        result.append(t)
    return result


def error_calculation(desired_vector, actual_vector):
    errors = 0
    for digit in range(len(desired_vector)):
        if actual_vector[digit] != desired_vector[digit]:
            errors += 1
    return errors


def learning(boolean_variable_sets, function_selection, search_minimum=None):
    weights = [0, 0, 0, 0, 0]
    number_era = 0
    table = PrettyTable()
    table.field_names = ['Era,k', 'Weights vector,W', 'Output vector,Y', 'Total error,E']
    plot_errors = []
    desired_vector = desired_boolean_vector(boolean_variable_sets)
    actual_vector = actual_boolean_vector(boolean_variable_sets, weights, function_selection)
    errors = error_calculation(desired_vector, actual_vector)
    plot_errors.append(errors)
    table.add_row([number_era, str(weights), actual_vector, errors])
    while True:
        number_era += 1
        desired_vector = []
        for value in boolean_variable_sets:
            t = boolean_function(value[1], value[2], value[3], value[4])
            y, net = evaluate_neural_network(value, weights, function_selection)
            desired_vector.append(t)
            error = t - y
            weights = correct_weights(value, error, weights, net, function_selection)
        actual_vector = actual_boolean_vector(boolean_variable_sets, weights, function_selection)
        errors = error_calculation(desired_vector, actual_vector)
        plot_errors.append(errors)
        table.add_row([number_era, str(weights), actual_vector, errors])
        if errors == 0:
            number_era += 1
            if search_minimum != 'yes':
                if function_selection == 'step':
                    plt.title("Step activation function")
                    plt.xlabel("k")
                    plt.ylabel("E")
                    plt.plot(range(number_era), plot_errors)
                    plt.show()
                else:
                    plt.title("Softsign activation function")
                    plt.xlabel("k")
                    plt.ylabel("E")
                    plt.plot(range(number_era), plot_errors)
                    plt.show()
                print(table)
            return weights


def search_minimum_set(boolean_variable_sets):
    weights = []
    combination_min = 200
    value_combination = []
    for number in range(1, 17):
        for combination in itertools.combinations(boolean_variable_sets, number):
            actual_result = []
            desired_result = []
            current_weights = learning(combination, 'softsign', 'yes')
            for value in boolean_variable_sets:
                actual_result.append(evaluate_neural_network(value, current_weights, False)[0])
                desired_result.append(boolean_function(value[1], value[2], value[3], value[4]))
            if actual_result == desired_result and len(combination) < combination_min:
                combination_min = len(combination)
                weights = current_weights
                value_combination = combination
    print('Minimum set:')
    for i in range(len(value_combination)):
        print('X', i + 1, ' = ', value_combination[i], ' ', sep='', end=' ')
    print()
    print("\nSynaptic coefficients:")
    print(weights)
    print('\nFull training required:')
    learning(value_combination, 'softsign')


if __name__ == '__main__':
    bool_values = value_table()
    print('STEP ACTIVATION FUNCTION:')
    learning(bool_values, 'step')
    print('\nSOFTSIGN ACTIVATION FUNCTION:')
    learning(bool_values, 'softsign')
    print('\nSEARCH FOR THE MINIMUM SET:\n')
    search_minimum_set(bool_values)
