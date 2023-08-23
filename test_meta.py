from abc import ABCMeta, abstractmethod
from typing import Type, TYPE_CHECKING


class MyDataMeta(ABCMeta):
    def __new__(cls, name, bases, attrs):
        fields = {}

        for base in bases:
            if hasattr(base, '__annotations__'):
                fields.update(base.__annotations__)

        fields.update(attrs.get('__annotations__', {}))

        def __init__(self, *args, **kwargs):
            for field, value in kwargs.items():
                setattr(self, field, value)

        attrs['__init__'] = __init__
        attrs.update(fields)

        cls: Type[MyClass] = super().__new__(cls, name, bases, attrs)

        return cls


class MyClass(metaclass=MyDataMeta):
    pass


class MySubclass(MyClass):
    z: int

    def my_method(self):
        print("MySubclass method")


obj = MySubclass(z='qdqwd')
print(obj.x)  # Output: 1
print(obj.y)  # Output: 2
print(obj.z)  # Output: 3
obj.my_method()  # Output: MySubclass method
