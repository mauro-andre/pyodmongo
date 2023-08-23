from pyodmongo import DbModel


class MyClass(DbModel):
    attr: str


print(MyClass.model_fields)
