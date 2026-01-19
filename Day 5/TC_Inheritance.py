class Animal:
    def speak(self):
        print("Animal makes a sound")
class Dog(Animal):
    def bark(self):
        print("dog barks")

d=Dog()
d.speak()
d.bark()
