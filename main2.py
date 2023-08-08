from fastapi import FastAPI
from pyodmondo_pv2 import Id, DbModel
from bson import ObjectId

app = FastAPI()

class Test(DbModel):
    var: str = 'Vrau'

@app.get('/')
async def test():
    obj = Test(id='64d19d2ea81f591eeb37823e')
    print(obj)
    
    