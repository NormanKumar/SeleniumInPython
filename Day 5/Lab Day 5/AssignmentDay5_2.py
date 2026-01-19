import math
class Calculator:
    def calculate(self,num1,num2):
        print("Calculator Addition:",num1+num2)

class AdvancedCalculator(Calculator):
    def calculate(self,num1,num2):
        print("Advance Calculator Multiplication:",num1*num2)

class number:
    def __init__(self,num):
        self.num=num
    def __add__(self, other):
        return number(self.num+other.num)
    def display(self):
        print(self.num)

cal=Calculator()
advCal=AdvancedCalculator()
cal.calculate(10,5)
advCal.calculate(10,5)
n1=number(10)
n2=number(20)
n3=n1+n2
n3.display()