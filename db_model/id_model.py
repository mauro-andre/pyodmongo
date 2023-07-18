from bson import ObjectId


class Id(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(v)
        except Exception as e:
            raise ValueError('invalid ObjectId')

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')
