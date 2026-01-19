class Vehicle:
    vehicle_count = 0
    def __init__(self):
        Vehicle.vehicle_count+=1
    def start(self):
        print("Vehicle started")

class car(Vehicle):
    def start(self):
        print("Car started")

class Bike(car):
    def start(self):
        print("Bike started")

v=Vehicle()
c=car()
b=Bike()

v.start()
c.start()
b.start()

print("Total vehicles created:", Vehicle.vehicle_count)