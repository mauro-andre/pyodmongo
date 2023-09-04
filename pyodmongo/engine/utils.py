from bson import ObjectId
from ..pydantic.main import BaseModel
from ..models.db_field_info import DbFieldInfo
from ..models.id_model import Id


def consolidate_dict(obj: BaseModel, dct: dict):
    for field in obj.model_fields.keys():
        value = getattr(obj, field)
        db_field_info: DbFieldInfo = getattr(obj.__class__, field)
        alias = db_field_info.field_alias
        has_model_fields = db_field_info.has_model_fields
        is_list = db_field_info.is_list
        by_reference = db_field_info.by_reference
        if has_model_fields:
            if value is None:
                dct[alias] = None
                continue
            if not is_list:
                if by_reference:
                    try:
                        dct[alias] = ObjectId(value.id)
                    except AttributeError:
                        dct[alias] = ObjectId(value)
                else:
                    dct[alias] = {}
                    consolidate_dict(obj=value, dct=dct[alias])
            else:
                if by_reference:
                    try:
                        dct[alias] = [ObjectId(o.id) for o in value]
                    except AttributeError:
                        dct[alias] = [ObjectId(o) for o in value]
                else:
                    dct[alias] = []
                    for v in value:
                        obj_lst_elem = {}
                        consolidate_dict(obj=v, dct=obj_lst_elem)
                        dct[alias].append(obj_lst_elem)
        else:
            if alias == 'id':
                alias = '_id'
            if db_field_info.field_type == Id:
                if is_list:
                    dct[alias] = [ObjectId(o) for o in value]
                else:
                    dct[alias] = ObjectId(value)
            else:
                dct[alias] = value
    return dct


def mount_base_pipeline(Model, query, populate: bool = False):
    match_stage = [{'$match': query}]
    model_stage = Model._pipeline
    reference_stage = Model._reference_pipeline
    if populate:
        return match_stage + model_stage + reference_stage
    else:
        return match_stage + model_stage
