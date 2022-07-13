class Vehicle():
    can_fly = False
    number_of_weels = 0

class Car(Vehicle):
    number_of_weels = 4

    def __init__(self, color):
        self.color = color

my_car = Car("red")
print(my_car.__dict__)
print(type(my_car))
# print(my_car.__base__.__dict__)