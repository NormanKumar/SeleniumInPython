class A:
    def showA(self):
        print("A")

class B:
    def showB(self):
        print("B")
    #     Overriding
    # def showA(self):
    #     print("A from class B")

class C(A,B):
    pass

c=C()
c.showA()
c.showB()
# c.showA()

