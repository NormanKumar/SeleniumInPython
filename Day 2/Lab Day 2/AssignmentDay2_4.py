class ValidateSalary:
    def __get__(self, instance, owner):
        return instance._salary

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("Salary must be a positive number")
        instance._salary = value

class Employee:
    salary = ValidateSalary()
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
emp1 = Employee("Alice", 50000)
print(emp1.name)
print(emp1.salary)
emp2 = Employee("Bob", -30000)
