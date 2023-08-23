from bson import ObjectId
from ..services.model_init import field_infos
from ..models.db_field_info import DbFieldInfo


def consolidate_dict(obj, dct: dict):
    for key in obj.model_fields.keys():
        value = getattr(obj, key)
        field_info: DbFieldInfo = field_infos(cls=obj, field_name=key)
        has_model_dump = field_info.is_pyodmongo_model
        is_list = field_info.is_list
        by_reference = field_info.by_reference
        if has_model_dump:
            if value is None:
                dct[key] = None
                continue
            if not is_list:
                if by_reference:
                    try:
                        dct[key] = ObjectId(value.id)
                    except AttributeError:
                        dct[key] = ObjectId(value)
                else:
                    dct[key] = {}
                    consolidate_dict(obj=value, dct=dct[key])
            else:
                if by_reference:
                    try:
                        dct[key] = [ObjectId(o.id) for o in value]
                    except AttributeError:
                        dct[key] = [ObjectId(o) for o in value]
                else:
                    dct[key] = []
                    for v in value:
                        obj_lst_elem = {}
                        consolidate_dict(obj=v, dct=obj_lst_elem)
                        dct[key].append(obj_lst_elem)
        else:
            if key == 'id':
                key = '_id'
            dct[key] = value
    return dct

def mount_base_pipeline(Model, query):
    match_stage = [{'$match': query}]
    model_stage = Model._pipeline
    reference_stage = Model._reference_pipeline
    return match_stage + model_stage + reference_stage