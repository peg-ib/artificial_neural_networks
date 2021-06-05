import math
import prettytable


def activation_function(net):
    return (1 - math.exp(-net)) / (1 + math.exp(-net))


def first_layer_delta(second_delta, weights, actual):
    first_delta = 0
    for position in range(len(weights)):
        first_delta += weights[position] * second_delta[position]
    return 0.5 * (1 - pow(actual, 2)) * first_delta


def second_layer_delta(desired, actual):
    return 0.5 * (1 - pow(actual, 2)) * (desired - actual)


class Neuron:
    def __init__(self, number_inputs, ny):
        self.number_inputs = number_inputs
        self.weights = [0.5] + [0] * number_inputs
        self.ny = ny

    def net(self, input_data):
        net = self.weights[0]
        for position in range(self.number_inputs):
            net += self.weights[position + 1] * input_data[position]
        return net

    def out(self, input_data):
        net = self.net(input_data)
        return activation_function(net)

    def correction(self, input_data, delta):
        self.weights[0] += self.ny * delta
        for position in range(len(input_data)):
            self.weights[position + 1] += self.ny * delta * input_data[position]
        return self.weights


class MultilayerNeuralNetwork:
    def __init__(self, structure, ny):
        self.structure = structure
        self.architecture = [[], []]
        for number in range(self.structure[1]):
            self.architecture[0].append(Neuron(self.structure[0], ny))
        for number in range(self.structure[2]):
            self.architecture[1].append(Neuron(self.structure[1], ny))

    def output(self, input_data):
        first_layer = []
        second_layer = []
        for perceptron in self.architecture[0]:
            first_layer.append(perceptron.out(input_data))
        for perceptron in self.architecture[1]:
            second_layer.append(perceptron.out(first_layer))
        return [first_layer, second_layer]

    def correction(self, input_data, first_layer, second_layer, desired):
        second_delta = []
        for element in range(len(second_layer)):
            second_delta.append(second_layer_delta(desired[element], second_layer[element]))
        for element in range(len(self.architecture[1])):
            self.architecture[1][element].correction(first_layer, second_delta[element])
        for first in range(self.structure[1]):
            weights = []
            for second in range(self.structure[2]):
                weights.append(self.architecture[1][second].weights[first + 1])
            self.architecture[0][first].correction(input_data, first_layer_delta(second_delta, weights,
                                                                                 first_layer[first]))


def learning(architect, input_data, output, ny):
    neural_network = MultilayerNeuralNetwork(architect, ny)
    table = prettytable.PrettyTable()
    table.field_names = ["Era", "Output", "Error"]
    era = 0
    while True:
        actual = neural_network.output(input_data)
        neural_network.correction(input_data, actual[0], actual[1], output)
        result = 0
        for i in range(len(actual[1])):
            result += pow((output[i] - actual[1][i]), 2)
        error = math.sqrt(result)
        table.add_row([era, *actual[1], error])
        era += 1
        if error < 0.0001:
            print(table)
            print("Weights:", neural_network.architecture[0][0].weights, neural_network.architecture[0][1].weights,
                  neural_network.architecture[1][0].weights)
            break


if __name__ == '__main__':
    learning([1, 2, 1], [-3], [-0.1], 1)
