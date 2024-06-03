from typing import Any
from types import NoneType


def _rec_verify(class_list: list) -> list:
    """
    Recursively verify the class hierarchy and extend the class list with base classes.

    Args:
        class_list (list): A list of classes to be verified.

    Returns:
        list: The extended list of classes including all base classes.
    """
    for cls in class_list:
        class_list += list(cls.__bases__)
    return class_list


def is_subclass(class_to_verify: Any, subclass: Any) -> bool:
    """
    Check if the class_to_verify is a subclass of the given subclass.

    Args:
        class_to_verify (Any): The class to be verified.
        subclass (Any): The subclass to check against.

    Returns:
        bool: True if class_to_verify is a subclass of subclass, otherwise False.
    """
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
