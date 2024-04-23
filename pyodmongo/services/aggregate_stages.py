def unwind(path: str, array_index: str, preserve_empty: bool):
    """
    Constructs an unwind stage for a MongoDB aggregation pipeline which deconstructs an array field
    from the input documents to output a document for each element.

    Args:
        path (str): The field path to an array to be unwound (without the '$' prefix).
        array_index (str): The name of a new field to hold the array index of the element.
        preserve_empty (bool): If True, includes the path as null on documents where the array is missing,
                                empty, or null; otherwise, such documents are excluded from the resulting
                                set.

    Returns:
        list[dict]: A list containing the unwind stage of the aggregation pipeline.

    Description:
        The unwind operation is useful for creating a flat view of array contents in order to apply
        further aggregation operations like match, project, or group.
    """
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
    """
    Constructs a lookup stage for a MongoDB aggregation pipeline which performs a join from another
    collection in the same database.

    Args:
        from_ (str): The target collection from which to fetch documents.
        local_field (str): The local field to match against the foreign field.
        foreign_field (str): The field from the documents of the "from" collection to match against.
        as_ (str): The output array field which contains the joined documents.
        pipeline (list): A list defining additional aggregation pipeline stages to filter the documents
                         from the "from" collection before joining.

    Returns:
        list[dict]: A list containing the lookup stage of the aggregation pipeline.

    Description:
        The lookup operation allows for integrating data from multiple collections based on a related field.
    """
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
    """
    Constructs a set stage for a MongoDB aggregation pipeline that redefines a field with a specified value.

    Args:
        as_ (str): The name of the field to redefine or create.

    Returns:
        list[dict]: A list containing the set stage of the aggregation pipeline.

    Description:
        This operation allows setting or replacing values of fields within documents during aggregation.
    """
    return [{"$set": {as_: {"$arrayElemAt": [f"${as_}", 0]}}}]


def group_set_replace_root(id_: str, field: str, path_str: str):
    """
    Constructs a combination of group, set, and replaceRoot stages for a MongoDB aggregation pipeline.

    Args:
        id_ (str): The field to use as the identifier for grouping documents.
        field (str): The field name to create or redefine with grouped values.
        path_str (str): The path string representing where to place or replace data in documents.

    Returns:
        list[dict]: A list containing the group, set, and replaceRoot stages of the aggregation pipeline.

    Description:
        This sequence of stages first groups documents by the specified identifier, aggregates
        specific fields, then modifies document structure, and finally promotes a nested document
        to the top-level.
    """
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
    """
    Constructs an unset stage for a MongoDB aggregation pipeline which removes the specified fields from documents.

    Args:
        fields (list): A list of field names to be removed from the documents.

    Returns:
        list[dict]: A list containing the unset stage of the aggregation pipeline.

    Description:
        The unset operation is used to delete fields from documents during aggregation, simplifying
        documents or removing unwanted data.
    """
    return [{"$unset": fields}]
