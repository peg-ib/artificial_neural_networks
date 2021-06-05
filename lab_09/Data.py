class Data:
    def __init__(self):
        self.global_points = []
        self.global_centroids = []
        self.metric = None
        self.coordinate_x = []
        self.coordinate_y = []
        self.number_point = 0
        self.number_centroid = 0

    def add_point(self, point):
        self.global_points.append(point)

    def add_centroids(self, centroid):
        self.global_centroids.append(centroid)

    def add_metric(self, metric):
        self.metric = metric

    def delete_metric(self):
        self.metric = None

    def delete_points(self):
        self.global_points = []

    def delete_centroids(self):
        self.global_centroids = []

    def delete_coordinate(self):
        self.coordinate_x = []
        self.coordinate_y = []

    def delete_number(self):
        self.number_point = 0
        self.number_centroid = 0

    def print_points(self):
        for point in self.global_points:
            coordinate = (point.x, point.y)
            print('x' + str(point.number), '=', coordinate)

    def print_centroids(self):
        for centroid in self.global_centroids:
            coordinate = (centroid.x, centroid.y)
            print('Centroid', centroid.color, '=', coordinate)
            self.coordinate_x.append(centroid.x)
            self.coordinate_y.append(centroid.y)
