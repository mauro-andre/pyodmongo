from fastapi import FastAPI
from fastapi.testclient import TestClient
from pyodmongo import DbModel

app = FastAPI()


class Model1(DbModel):
    attr1: str = None
    attr2: str


class Model2(Model1):
    attr3: str
    attr4: str = None


@app.post("/", response_model=Model2)
async def read_main(input_obj: Model2):
    return input_obj


client = TestClient(app)


def test_response_model_and_output_obj():
    json_body = {
        "attr2": "Value 2",
        "attr3": "Value 3",
    }
    response = client.post(url="/", json=json_body)
    assert response.status_code == 200
    assert response.json() == {
        "id": None,
        "created_at": None,
        "updated_at": None,
        "attr1": None,
        "attr2": "Value 2",
        "attr3": "Value 3",
        "attr4": None,
    }
