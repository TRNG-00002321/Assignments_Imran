#Create a class shape with a method that returns the area
#Inherit the shape class to circle, rectangle, and triangle classes
#Calculate the area and print the result
#return not print
import math
class shape():
    def area(self):
        print("Area of shape")

class circle(shape):
    def area(self):
        r = float(input("Enter the radius of the circle: "))
        area = math.pi * r ** 2
        print("Area = ", area)

class rectangle(shape):
    def area(self):
        l = float(input("enter length:"))
        w = float(input("enter width:"))
        area = l * w
        print("Area = ", area)

class triangle(shape):
    def area(self):
        b = float(input("Enter base: "))
        h = float(input("Enter height: "))
        area = 0.5 * b * h
        print("Area =", area)

c = circle()
c.area()

r = rectangle()
r.area()

t = triangle()
t.area()
