from fastapi import HTTPException


async def delete(Model, query):
    try:
        result = await Model.collection().delete_one(filter=query)
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail='Id not found')
        return {'message': 'Success delete'}
    except TypeError as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)