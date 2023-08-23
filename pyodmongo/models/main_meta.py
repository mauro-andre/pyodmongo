from abc import ABCMeta
from datetime import datetime
import sys
from typing import Dict, List


class DbMeta(ABCMeta):
    def __new__(cls, name, bases, namespace):
        attributes = namespace.get('__annotations__', {})

        init_method = DbMeta.__get_init_method(attributes)
        exec(init_method,
             sys.modules[namespace['__module__']].__dict__, namespace)

        return super().__new__(cls, name, bases, namespace)

    @staticmethod
    def __get_function_string(name, args: List[str], body: List[str]) -> str:
        signature = ', '.join(args)
        body_content = '\n\t'.join(body) or 'pass'
        return f'def {name}({signature}):\n\t{body_content}'

    @staticmethod
    def __get_init_method(attributes: Dict[str, type]) -> str:
        init_params = ['self'] + list(attributes.keys())
        body = [f'self.{arg} = {arg}' for arg in attributes]
        return DbMeta.__get_function_string('__init__', init_params, body)


class DbModel(metaclass=DbMeta):
    id: str
    created_at: datetime
    updates_at: datetime

    # def __init__(self, id_init, created_at_init, updated_at_init):
    #     self.id_init = id_init
    #     self.created_at_init = created_at_init
    #     self.updated_at_init = updated_at_init
