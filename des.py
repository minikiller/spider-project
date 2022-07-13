class Name:
    def __get__(self, instance, owner=None):
        print(f'__get__,instance is {instance},owner is {owner}')
        return "peter"

class A:
    name=Name()
    # def __init__(self) -> None:
    #     self.name=Name()

o=A()

# print(A.name)
Name.__set__=lambda x,y,z:None
o.name="Bob"
print(o.name)