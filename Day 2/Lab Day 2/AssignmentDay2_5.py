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
print(emp1.name, emp1.salary)
emp2 = Employee("Bob", 70000)
print(emp2.name, emp2.salary)
emp3 = Employee("Charlie", -30000)

