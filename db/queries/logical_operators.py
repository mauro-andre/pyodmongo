def and_(operators: list):
    return {'$and': operators}


def or_(operators: list):
    return {'$or': operators}
