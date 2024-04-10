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


def lookup(from_: str, local_field: str, foreign_field: str, as_: str, pipeline: list):
    return [
        {
            "$lookup": {
                "from": from_,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_,
                "pipeline": pipeline,
            }
        }
    ]


def set_(as_: str):
    return [{"$set": {as_: {"$arrayElemAt": [f"${as_}", 0]}}}]


def group_set_replace_root(id_: str, field: str, path_str: str):
    return [
        {
            "$group": {
                "_id": f"${id_}",
                "_document": {"$first": "$$ROOT"},
                field: {"$push": f"${path_str}"},
            }
        },
        {"$set": {f"_document.{path_str}": f"${field}"}},
        {"$replaceRoot": {"newRoot": "$_document"}},
    ]


def unset(fields: list):
    return [{"$unset": fields}]
