import pytest
from pyodmongo import AsyncDbEngine, DbEngine
from datetime import timezone, timedelta


mongo_uri = "mongodb://localhost:27017"
db_name = "pyodmongo_pytest"
tz_info = timezone(timedelta(hours=-3))


@pytest.fixture
def async_engine():
    yield AsyncDbEngine(mongo_uri=mongo_uri, db_name=db_name, tz_info=tz_info)


@pytest.fixture
def engine():
    return DbEngine(mongo_uri=mongo_uri, db_name=db_name, tz_info=tz_info)
