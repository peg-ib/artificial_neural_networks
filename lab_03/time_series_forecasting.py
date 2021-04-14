import math
import matplotlib.pyplot as plt
from decimal import Decimal


def function(x):
    return math.sin(0.1 * (x ** 3) - 0.2 * (x ** 2) + x - 1)


def change_interval(left, right):
    coordinate_x = coordinate(left, right, 20)
    delta = coordinate_x[1] - coordinate_x[0]
    buf = left
    left = right + delta
    right = 2 * right - buf
    return left, right


def calculation_delta(desired, actual):
    return desired - actual


def coordinate(left, right, number):
    distance = (right - left) / number
    xi = left
    coordinate_x = [xi]
    while xi != right:
        xi += distance
        xi = round(xi, 2)
        coordinate_x.append(xi)
    return coordinate_x


def calculation_desired_function(left, right):
    desired_function = []
    coordinate_x = coordinate(left, right, 20)
    for value in coordinate_x:
        desired_function.append(function(value))
    return desired_function


def error_calculation(desired, actual):
    error = 0
    for index in range(len(desired)):
        desired[index] = Decimal(desired[index])
        actual[index] = Decimal(actual[index])
        error += (desired[index] - actual[index]) ** 2
    error = math.sqrt(error)
    return error


def correct_weights(weights, ny, delta, values):
    weights[0] += ny * delta
    for iteration in range(len(weights) - 1):
        weights[iteration + 1] += ny * delta * values[iteration]
    return weights


def evaluate_neural_network(input_data, weights):
    net = weights[0]
    for index in range(len(input_data)):
        net += weights[index + 1] * input_data[index]
    return net


def learning(number_epochs, ny, window_size, left, right):
    weights = []
    while len(weights) != window_size + 1:
        weights.append(0)
    desired_function = calculation_desired_function(left, right)
    era = 0
    while era != number_epochs:
        window = desired_function[:window_size]
        for step in range(len(desired_function) - window_size):
            new_element = evaluate_neural_network(window, weights)
            delta = calculation_delta(desired_function[window_size + step], new_element)
            weights = correct_weights(weights, ny, delta, window)
            window.append(desired_function[window_size + step])
            window = window[1:]
        era += 1
    return weights


def completion_function(weights, left, right, window_size):
    desired_function = calculation_desired_function(left, right)
    window = desired_function[len(desired_function) - window_size:]
    left, right = change_interval(left, right)
    desired_function = calculation_desired_function(left, right)
    actual_function = []
    for step in range(len(desired_function)):
        new_window_element = evaluate_neural_network(window, weights)
        actual_function.append(new_window_element)
        window.append(new_window_element)
        window = window[1:]
    error = error_calculation(desired_function, actual_function)
    return error, actual_function


def plot(coordinate_x, desired_function, actual_function, line):
    fig, ax = plt.subplots()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.plot(coordinate_x, desired_function, coordinate_x, actual_function)
    ax.grid()
    ax.vlines(line, min(desired_function), max(desired_function), color='r')
    plt.show()


def research(left, right, number_era, ny, window_size):
    # error dependence on epochs
    errors = []
    number_epochs = []
    for era in range(500, 10500, 500):
        weights = learning(era, ny, window_size, left, right)
        error, actual_function = completion_function(weights, left, right, window_size)
        number_epochs.append(era)
        errors.append(error)
    plt.xlabel("M")
    plt.ylabel("E")
    plt.plot(number_epochs, errors)
    plt.show()
    # dependence of error on window size
    errors = []
    windows = []
    for window in range(2, 20):
        weights = learning(number_era, ny, window, left, right)
        error, actual_function = completion_function(weights, left, right, window)
        windows.append(window)
        errors.append(error)
    plt.xlabel("P")
    plt.ylabel("E")
    plt.plot(windows, errors)
    plt.show()
    # dependence of error on learning rate
    errors = []
    number_ny = []
    for ny in range(10, 105, 5):
        weights = learning(number_era, ny / 100, window_size, left, right)
        error, actual_function = completion_function(weights, left, right, window_size)
        number_ny.append(ny / 100)
        errors.append(error)
    plt.xlabel("ny")
    plt.ylabel("E")
    plt.plot(number_ny, errors)
    plt.show()


def print_result(left, right, number_era, ny, window_size):
    buf = left
    result_weights = learning(number_era, ny, window_size, left, right)
    result_error, actual_function = completion_function(result_weights, left, right, window_size)
    desired_function_left = calculation_desired_function(left, right)
    left_coordinate = coordinate(left, right, 20)
    left, right = change_interval(left, right)
    desired_function_right = calculation_desired_function(left, right)
    right_coordinate = coordinate(left, right, 20)
    coordinate_x = left_coordinate + right_coordinate
    desired_function = desired_function_left + desired_function_right
    new_function = desired_function_left + actual_function
    area = right - (right - buf) / 2
    plot(coordinate_x, desired_function, new_function, area)
    print('number of epochs = ', number_era)
    print('window size = ', window_size)
    print('ny = ', ny)
    print("synaptic weights:", result_weights)
    print("error = ", result_error)


def brute_force(left, right):
    number_era = 0
    window = 0
    ny = 0
    error = 200
    weights = []
    for current_number_era in range(500, 10500, 500):
        for current_window in range(2, 20):
            for current_ny in range(10, 105, 5):
                print("M =", current_number_era, "p =", current_window, "ny =", current_ny / 100)
                current_weights = learning(current_number_era, current_ny / 100, current_window, left, right)
                print(current_weights)
                current_error, actual_function = completion_function(current_weights, left, right, current_window)
                print(current_error)
                if current_error <= error:
                    number_era = current_number_era
                    window = current_window
                    ny = current_ny
                    error = current_error
                    weights = current_weights
    print(number_era)
    print(window)
    print(ny)
    print(error)
    print(weights)


if __name__ == '__main__':
    brute_force(0, 1)
    print_result(0, 1, 4000, 0.9, 4)
    # research(0, 1, 4000, 0.9, 4)
