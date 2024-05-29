import pydantic
import platform
import sys
import pymongo
import motor
from pyodmongo import version


def test_version():
    info = {
        "PyODMongo version": "__VERSION__",
        "Pydantic version": pydantic.version.VERSION,
        "Pymongo version": pymongo.__version__,
        "Motor version": motor._version.version,
        "Python version": sys.version,
        "Platform": platform.platform(),
    }
    response_expected = "\n".join([f"{key}: {value}" for key, value in info.items()])
    assert response_expected == version.response
