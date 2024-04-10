def unwind(path: str, array_index: str, preserve_empty: bool):
    return [
        {
            "$unwind": {
                "path": f"${path}",
                "includeArrayIndex": array_index,
                "preserveNullAndEmptyArrays": preserve_empty,
            }
        }
    ]


def lookup(_from: str, local_field: str, foreign_field: str, _as: str, pipeline: list):
    return [
        {
            "$lookup": {
                "from": _from,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": _as,
                "pipeline": pipeline,
            }
        }
    ]


def _set(_as: str):
    return [{"$set": {_as: {"$arrayElemAt": [f"${_as}", 0]}}}]


def group_set_replace_root(_id: str, field: str, path_str: str):
    return [
        {
            "$group": {
                "_id": f"${_id}",
                "_document": {"$first": "$$ROOT"},
                field: {"$push": f"${path_str}"},
            }
        },
        {"$set": {f"_document.{path_str}": f"${field}"}},
        {"$replaceRoot": {"newRoot": "$_document"}},
    ]


def unset(fields: list):
    return [{"$unset": fields}]
