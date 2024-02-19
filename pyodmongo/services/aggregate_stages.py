def lookup_and_set(
    from_: str,
    local_field: str,
    foreign_field: str,
    as_: str,
    pipeline: list,
    is_reference_list: bool,
):
    lookup_stage = [
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
    set_stage = [{"$set": {as_: {"$arrayElemAt": [f"${as_}", 0]}}}]
    if is_reference_list:
        return lookup_stage
    return lookup_stage + set_stage
