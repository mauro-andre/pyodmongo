from bson import ObjectId
from pprint import pprint
from db_model import save, find_one
from fastapi import FastAPI
from models import BrazilianCity, Address, Integrator

app = FastAPI()


# address = Address(street='Rua dos bobos', number='123')
# integrator = Integrator(id=ObjectId('64add18355e21f9d756d95c8'), name='Integrador Legal 2',
#                         email='shunda1@email.com', address=address)
# user = User(username='Shunda', phone_number='99999', integrator=integrator)


@app.get('/test')
async def test():
    # query = {'_id': ObjectId('64ae98b4e818b4d3b46757f5')}
    # city = await find_one(Model=BrazilianCity, query=query)
    # address = Address(street='Rua Muito Legal', number='123ABC', city=city)
    # integrator = Integrator(name='Integrador Muito bacanudo', address=address)
    # await save(integrator)

    query = {'_id': ObjectId('64af393a5dbf1f2bd3842a4b')}
    integrator = await find_one(Model=Integrator, query=query)
    return integrator
# class Test(BaseModel):
#     id: str
#     name: str


# obj_dict = {'_id': 'a1b2c3', 'name': 'Shunda'}
# obj = Test(**obj_dict)
# obj_to_dict = obj.dict()
