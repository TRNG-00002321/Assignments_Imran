from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def shape(self):
        pass

class Circle(Shape):
    def shape(self):
        return "Rectangle"

circle = Circle()
print(circle.shape())
rectangle = Shape()
print(rectangle.shape())