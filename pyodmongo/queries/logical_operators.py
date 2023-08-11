def and_(*operators):
    return {'$and': list(operators)}


def or_(*operators):
    return {'$or': list(operators)}
