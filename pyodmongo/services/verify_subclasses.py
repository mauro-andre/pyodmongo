from typing import Any
from types import NoneType


def _rec_verify(class_list: list):
    for cls in class_list:
        class_list += list(cls.__bases__)
    return class_list


def is_subclass(class_to_verify: Any, subclass: Any):
    if class_to_verify is NoneType:
        return True
    if (
        class_to_verify is NoneType
        or class_to_verify is None
        or class_to_verify is subclass
    ):
        return True
    subclasses = _rec_verify(class_list=list(class_to_verify.__bases__))
    return subclass in subclasses
