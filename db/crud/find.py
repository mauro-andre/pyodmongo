from fastapi import HTTPException
from ..services.connection import db
from asyncio import gather
from math import ceil
from ..models.paginate import ResponsePaginate


async def __aggregate(Model, pipeline):
    docs_cursor = db[Model._collection].aggregate(pipeline)
    return [Model(**doc) async for doc in docs_cursor]


def __mount_base_pipeline(Model, query):
    match_stage = [{'$match': query}]
    model_stage = Model._pipeline
    reference_stage = Model._reference_pipeline
    return match_stage + model_stage + reference_stage


async def __resolve_count_pipeline(Model, pipeline):
    docs = await db[Model._collection].aggregate(pipeline).to_list(1)
    try:
        count = docs[0]['count']
        return count
    except IndexError as e:
        return 0


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


async def find_many(Model, query, current_page: int, docs_per_page: int):
    max_docs_per_page = 1000
    current_page = 1 if current_page <= 0 else current_page
    docs_per_page = max_docs_per_page if docs_per_page > max_docs_per_page else docs_per_page

    count_stage = [{'$count': 'count'}]
    skip = (docs_per_page * current_page) - docs_per_page
    skip_stage = [{'$skip': skip}]
    limit_stage = [{'$limit': docs_per_page}]

    pipeline = __mount_base_pipeline(Model=Model, query=query)
    count_pipeline = pipeline + count_stage
    result_pipeline = pipeline + skip_stage + limit_stage

    result, count = await gather(__aggregate(Model=Model, pipeline=result_pipeline),
                                 __resolve_count_pipeline(Model=Model, pipeline=count_pipeline))

    page_quantity = ceil(count / docs_per_page)
    return ResponsePaginate(current_page=current_page,
                            page_quantity=page_quantity,
                            docs_quantity=count,
                            docs=result)


async def populate(objs: list):
    ids = [obj.id for obj in objs]
    Model = type(objs[0])
    pipeline = __mount_base_pipeline(
        Model=Model, query={'_id': {'$in': ids}}
    )
    objs = await __aggregate(Model=Model, pipeline=pipeline)
    return objs
