class Student:
    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no

    def display_details(self):
        print("Name:",self.name)
        print("Roll:",self.roll_no)

student1 = Student("Rahul Sharma", 1)
student2 = Student("Anubhav Gupta", 2)

student1.display_details()
student2.display_details()
