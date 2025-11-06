class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello my name is, {self.name}")

    def __str__(self):
        return (f"{self.name} is {self.age} years old")

p1 = Person("John", 25)
p1.greet()

print(p1)