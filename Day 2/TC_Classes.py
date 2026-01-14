class Student:
    name = "Ravi"
    age = 25
s1 =Student()
print(s1.name)
print(s1.age)

class Employee:
    def __init__(self,name,age):
        self.name = name
        self.age = age
e1 = Employee("Ravi",25)
print(e1.name)
print(e1.age)