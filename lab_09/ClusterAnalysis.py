from math import sqrt


def euclidean_distance(centroid, point):
    return sqrt(pow((centroid.x - point.x), 2) + pow((centroid.y - point.y), 2))


def chebyshev_distance(centroid, point):
    return max(abs(centroid.x - point.x), abs(centroid.y - point.y))


def distance_calculation(distance, centroid, point):
    current_distance = None
    if distance == 'Euclidean':
        current_distance = euclidean_distance(centroid, point)
    elif distance == 'Chebyshev':
        current_distance = chebyshev_distance(centroid, point)
    return current_distance


class ClusterAnalysis:
    def __init__(self, centroids, points, metric):
        self.centroids = centroids
        self.points = points
        self.metric = metric
        self.coordinate_x = []
        self.coordinate_y = []

    def cluster_creation(self):
        clusters = {}
        distance = None
        current_centroid = None
        for point in self.points:
            for number_centroid in range(len(self.centroids)):
                current_distance = distance_calculation(self.metric, self.centroids[number_centroid], point)
                if number_centroid == 0:
                    distance = current_distance
                if current_distance <= distance:
                    distance = current_distance
                    point.color = self.centroids[number_centroid].color
                    current_centroid = self.centroids[number_centroid]
                if number_centroid == len(self.centroids) - 1:
                    if current_centroid in clusters:
                        clusters[current_centroid].append(point)
                    else:
                        clusters[current_centroid] = [point]
        return clusters

    def move_centroid(self, clusters):
        for cluster in clusters:
            sum_x = 0
            sum_y = 0
            for point in clusters[cluster]:
                sum_x += point.x
                sum_y += point.y
            cluster.x = sum_x / len(clusters[cluster])
            cluster.y = sum_y / len(clusters[cluster])
            for centroid in self.centroids:
                if centroid == cluster:
                    centroid.x = cluster.x
                    centroid.y = cluster.y

    def is_end(self):
        x = []
        y = []
        if self.coordinate_x and self.coordinate_y:
            for centroid in self.centroids:
                x.append(centroid.x)
                y.append(centroid.y)
            if self.coordinate_x == x and self.coordinate_y == y:
                return True
            else:
                self.coordinate_x = []
                self.coordinate_y = []
                return False
        else:
            return False

    def k_means(self):
        if self.is_end():
            clusters = self.cluster_creation()
            print('Metric:', self.metric)
            for centroid, points in clusters.items():
                number_point = []
                for point in points:
                    number_point.append('x' + str(point.number))
                coordinate = (centroid.x, centroid.y)
                print('Coordinates of the', centroid.color, 'centroid:', coordinate)
                print('Centroid {0}: {1}'.format(centroid.color, number_point))
            print()
        for number_centroids in range(len(self.centroids)):
            self.coordinate_x.append(self.centroids[number_centroids].x)
            self.coordinate_y.append(self.centroids[number_centroids].y)
        clusters = self.cluster_creation()
        self.move_centroid(clusters)
