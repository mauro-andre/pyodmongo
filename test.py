from pydantic import BaseModel


class Mae(BaseModel):
    id: str
    created_at: str = None

    def __init__(self, **attrs):
        attrs['id'] = attrs.pop('_id')
        print(attrs)
        super().__init__(**attrs)


class Filho(Mae):
    var1: str
    var2: str


obj_dict = {'_id': 'a1b2c3', 'var1': 'Vrau 1', 'var2': 'Vrau 2'}
obj = Filho(**obj_dict)
obj_to_dict = obj.dict()
print(obj_to_dict)
