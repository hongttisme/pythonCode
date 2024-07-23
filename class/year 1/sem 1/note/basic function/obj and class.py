import math


class Circle:
    def __init__(self, r=1):
        self.radius = r
        self.__me = 10

    def get_area(self):
        return self.radius * self.radius * math.pi

    def get_dim(self, y):
        self.radius = y
        return 0

    def get_me(self):
        return self.__me


c1 = Circle(2)
print(c1.get_area())
c1.get_dim(1)
print(c1.get_area())
print(c1.get_me())
