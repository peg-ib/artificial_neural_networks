class Point:
    def __init__(self, x, y, color, number):
        self.x = x
        self.y = y
        self.color = color
        self.number = number

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

