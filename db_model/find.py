from fastapi import HTTPException
from .connection import db


async def __aggregate(Model, pipeline):
    docs_cursor = db[Model._collection].aggregate(pipeline)
    return [Model(**doc) async for doc in docs_cursor]


def __mount_base_pipeline(Model, query):
    match_stage = [{'$match': query}]
    model_stage = Model._pipeline
    reference_stage = Model._reference_pipeline
    return match_stage + model_stage + reference_stage


async def find_one(Model, query):
    pipeline = __mount_base_pipeline(Model=Model, query=query)
    pipeline += [{'$limit': 1}]
    try:
        result = await __aggregate(Model=Model, pipeline=pipeline)
        return result[0]
    except TypeError as e:
        raise HTTPException(status_code=404, detail='no records found')
    except AttributeError as e:
        raise HTTPException(status_code=400, detail='Id not found')
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


async def find_many(Model, query):
    pass
