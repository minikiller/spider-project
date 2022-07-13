class Verbose_attribute():
    def __init__(self,val) -> None:
        self.value=val

    def __get__(self, obj, type=None) -> object:
        print("accessing the attribute to get the value")
        
        return self.value
    def __set__(self, obj, value) -> None:
        print("accessing the attribute to set the value")
        self.value=value
        # raise AttributeError("Cannot change the value")

class Foo():
    attribute1 = Verbose_attribute(12)

my_foo_object = Foo()
x = my_foo_object.attribute1
print(x)

my_foo_object.attribute1=120
# x = 
print(my_foo_object.attribute1)