class ExplainDescriptors:
    def __init__(self):
        print('__init__')

    def __set_name__(self, owner, name):
        print(f'__set_name__(owner={owner}, name={name})')
        self.name = name

    def __get__(self, instance, owner=None):
        print(f'__get__(instance={instance}, owner={owner})')
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        print(f'__set__(instance={instance}, value={value})')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        print(f'__delete__(instance={instance})')
        del instance.__dict__[self.name]

class SomeClass:
    a=ExplainDescriptors()

some=SomeClass()
# some.a=10
# print(some.a)