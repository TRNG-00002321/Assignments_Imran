class Animal:
    def speak(self):
        print("Animal speaks")


class dog(Animal):
    def speak(self):
        print("Dog speaks")


d = dog()
d.speak()