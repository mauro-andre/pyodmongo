from pyodmongo import Id, DbModel


def test_id_model():
    class MyClass(DbModel):
        my_id: Id

    obj = MyClass(my_id=None)
    assert obj.my_id == None
