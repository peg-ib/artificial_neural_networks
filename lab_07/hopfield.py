import numpy as np


def sign(net):
    return 1 if net > 0 else -1


class NeuralNetwork:
    def __init__(self, length_data):
        self.length_data = length_data
        self.weights = np.zeros((length_data, length_data), int)

    def learning(self, data):
        for image in range(len(data)):
            for i in range(len(data[0])):
                for j in range(len(data[0])):
                    if i != j:
                        self.weights[i][j] += data[image][i] * data[image][j]
        return self.weights

    def convergence(self, data):
        epochs = np.array([data])
        while True:
            image = np.dot(self.weights, data)  # перемножение матриц
            for index in range(len(image)):
                if image[index] != 0:
                    image[index] = sign(image[index])
                else:
                    image[index] = data[index]
            data = image
            epochs = np.append(epochs, [data], axis=0)
            if len(epochs) == 4:
                if np.array_equal(epochs[3], epochs[1]) and np.array_equal(epochs[2], epochs[0]):
                    return epochs[3]
                else:
                    epochs = epochs[1:]
            else:
                continue


def print_image(image):
    matrix = []
    for element in image:
        if element == 1:
            matrix.append(chr(11035))
        elif element == -1:
            matrix.append(chr(11036))
    for index in range(5):
        line = [matrix[0:5][index], matrix[5:10][index], matrix[10:15][index], matrix[15:20][index]]
        print(*line)
    print()


def hopfield_network(input_images, input_modified_images):
    network = NeuralNetwork(len(input_modified_images[0]))
    weights = network.learning(input_images)
    print('Hopfield RNN weights:')
    print(weights)
    print()
    restored_images = []
    for image in input_modified_images:
        restored_images.append(network.convergence(image))
    print('IMAGE:', 2)
    print('Input data:')
    print_image(input_modified_images[0])
    print('Result:')
    print_image(restored_images[0])
    print('IMAGE:', 4)
    print('Input data:')
    print_image(input_modified_images[1])
    print('Result:')
    print_image(restored_images[1])
    print('IMAGE:', 8)
    print('Input data:')
    print_image(input_modified_images[2])
    print('Result:')
    print_image(restored_images[2])


if __name__ == '__main__':
    first_image = [1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1]
    second_image = [1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1]
    third_image = [1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1]
    images = [first_image, second_image, third_image]
    first_modified_image = [1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, -1, 1]
    second_modified_image = [-1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1]
    third_modified_image = [1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 1]
    modified_image = [first_modified_image, second_modified_image, third_modified_image]
    hopfield_network(images, modified_image)
