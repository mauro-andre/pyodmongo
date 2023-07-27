from pydantic import BaseModel


class MainModel(BaseModel):
    class Config:
        anystr_strip_whitespace = True
