class Maiyou(object):

    a = 0
    b = 1

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def normal_func(self):
        print('普通的函数')

    @staticmethod
    def static_func():
        print('静态函数')

    @classmethod
    def class_func(cls):
        print('类函数')


if __name__ == '__main__':
    print('类的__dict__:')
    print( Maiyou.__dict__)
    print()

    obj = Maiyou('zhangsan', 18)
    print('对象的__dict__:')
    print(obj.__dict__)
    # print(Maiyou.static_func())