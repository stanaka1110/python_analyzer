class Base1:
    def func1(self):
        print('func1')
     
class Sub(Base1):
    def func(self):
        super().func1()

obj = Sub()
obj.func()