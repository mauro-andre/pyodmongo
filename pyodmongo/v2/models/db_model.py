from ..metaclasses.main_meta import MainMeta
from pydantic import BaseModel


class DbModel(BaseModel, metaclass=MainMeta): ...
