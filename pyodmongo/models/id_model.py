class Id(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return str(v)
        except Exception as e:
            raise ValueError('invalid Id')
