from ..models.db_model import MainBaseModel, DbModel
from ..models.db_field import DbField


def consolidate_dict(obj: DbModel, dct: dict) -> dict:
    print(obj.model_dump())
    # model = obj.__class__
    # db_fields: dict[str, DbField] = model.__db_fields__
    # for db_field in db_fields.values():
    #     value = getattr(obj, db_field.field_name)
    #     print(db_field.field_name, value)
    #     print(db_field)
    #     print()
