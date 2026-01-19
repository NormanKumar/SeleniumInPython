class animal:
    def sound(self):
        print("animal sound")
class dog(animal):
    def sound(self):
        print("dog Barks")
class cat(animal):
    def sound(self):
        print("cat meows")

obj=[animal(),dog(),cat()]
for a in obj:
    a.sound()
