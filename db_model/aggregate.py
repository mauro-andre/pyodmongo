def lookup(from_: str, local_field: str, foreign_field: str, as_: str):
    return {
        '$lookup': {
            'from': from_,
            'localField': local_field,
            'foreignField': foreign_field,
            'as': as_
        }
    }
