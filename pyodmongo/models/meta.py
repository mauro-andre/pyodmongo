"""Private logic for creating models."""
from __future__ import annotations as _annotations
from pydantic._internal._model_construction import (ModelMetaclass,
                                                    inspect_namespace,
                                                    init_private_attributes,
                                                    set_default_hash_func,
                                                    complete_model_class,
                                                    unpack_lenient_weakvaluedict,
                                                    build_lenient_weakvaluedict)


import typing
import warnings
from abc import ABCMeta
from types import FunctionType
from typing import Any, Generic

from pydantic_core import PydanticUndefined
from typing_extensions import dataclass_transform

from pydantic.fields import Field, FieldInfo
from pydantic.warnings import PydanticDeprecatedSince20
from pydantic._internal._config import ConfigWrapper
from pydantic._internal._decorators import ComputedFieldInfo, DecoratorInfos, PydanticDescriptorProxy
from pydantic._internal._fields import is_valid_field_name, _is_finalvar_with_default_val
from pydantic._internal._generics import PydanticGenericMetadata, get_model_typevars_map
from pydantic._internal._typing_extra import get_cls_types_namespace, is_classvar, parent_frame_namespace
from pydantic._internal._validate_call import ValidateCallWrapper
from pydantic._internal._typing_extra import get_cls_type_hints_lenient
from copy import copy

if typing.TYPE_CHECKING:
    from .main import BaseModel
    from .main import DbModel
else:
    # See PyCharm issues https://youtrack.jetbrains.com/issue/PY-21915
    # and https://youtrack.jetbrains.com/issue/PY-51428
    DeprecationWarning = PydanticDeprecatedSince20


IGNORED_TYPES: tuple[Any, ...] = (
    FunctionType,
    property,
    classmethod,
    staticmethod,
    PydanticDescriptorProxy,
    ComputedFieldInfo,
    ValidateCallWrapper,
)

object_setattr = object.__setattr__


@dataclass_transform(kw_only_default=True, field_specifiers=(Field,))
class PyODMongoMeta(ModelMetaclass, ABCMeta):
    def __new__(
        mcs,
        cls_name: str,
        bases: tuple[type[Any], ...],
        namespace: dict[str, Any],
        __pydantic_generic_metadata__: PydanticGenericMetadata | None = None,
        __pydantic_reset_parent_namespace__: bool = True,
        **kwargs: Any,
    ) -> type:
        """Metaclass for creating Pydantic models.

        Args:
            cls_name: The name of the class to be created.
            bases: The base classes of the class to be created.
            namespace: The attribute dictionary of the class to be created.
            __pydantic_generic_metadata__: Metadata for generic models.
            __pydantic_reset_parent_namespace__: Reset parent namespace.
            **kwargs: Catch-all for any other keyword arguments.

        Returns:
            The new class created by the metaclass.
        """
        # Note `ModelMetaclass` refers to `BaseModel`, but is also used to *create* `BaseModel`, so we rely on the fact
        # that `BaseModel` itself won't have any bases, but any subclass of it will, to determine whether the `__new__`
        # call we're in the middle of is for the `BaseModel` class.
        if bases:
            base_field_names, class_vars, base_private_attributes = mcs._collect_bases_data(bases)

            config_wrapper = ConfigWrapper.for_model(bases, namespace, kwargs)
            namespace['model_config'] = config_wrapper.config_dict
            private_attributes = inspect_namespace(
                namespace, config_wrapper.ignored_types, class_vars, base_field_names
            )
            if private_attributes:
                if 'model_post_init' in namespace:
                    # if there are private_attributes and a model_post_init function, we handle both
                    original_model_post_init = namespace['model_post_init']

                    def wrapped_model_post_init(self: BaseModel, __context: Any) -> None:
                        """We need to both initialize private attributes and call the user-defined model_post_init
                        method.
                        """
                        init_private_attributes(self, __context)
                        original_model_post_init(self, __context)

                    namespace['model_post_init'] = wrapped_model_post_init
                else:
                    namespace['model_post_init'] = init_private_attributes

            namespace['__class_vars__'] = class_vars
            namespace['__private_attributes__'] = {**base_private_attributes, **private_attributes}

            if config_wrapper.frozen:
                set_default_hash_func(namespace, bases)
            cls: type[DbModel] = ABCMeta.__new__(mcs, cls_name, bases, namespace, **kwargs)  # type: ignore

            from .main import BaseModel

            cls.__pydantic_custom_init__ = not getattr(cls.__init__, '__pydantic_base_init__', False)
            cls.__pydantic_post_init__ = None if cls.model_post_init is BaseModel.model_post_init else 'model_post_init'

            cls.__pydantic_decorators__ = DecoratorInfos.build(cls)

            # Use the getattr below to grab the __parameters__ from the `typing.Generic` parent class
            if __pydantic_generic_metadata__:
                cls.__pydantic_generic_metadata__ = __pydantic_generic_metadata__
            else:
                parent_parameters = getattr(cls, '__pydantic_generic_metadata__', {}).get('parameters', ())
                parameters = getattr(cls, '__parameters__', None) or parent_parameters
                if parameters and parent_parameters and not all(x in parameters for x in parent_parameters):
                    combined_parameters = parent_parameters + tuple(x for x in parameters if x not in parent_parameters)
                    parameters_str = ', '.join([str(x) for x in combined_parameters])
                    generic_type_label = f'typing.Generic[{parameters_str}]'
                    error_message = (
                        f'All parameters must be present on typing.Generic;'
                        f' you should inherit from {generic_type_label}.'
                    )
                    if Generic not in bases:  # pragma: no cover
                        # We raise an error here not because it is desirable, but because some cases are mishandled.
                        # It would be nice to remove this error and still have things behave as expected, it's just
                        # challenging because we are using a custom `__class_getitem__` to parametrize generic models,
                        # and not returning a typing._GenericAlias from it.
                        bases_str = ', '.join([x.__name__ for x in bases] + [generic_type_label])
                        error_message += (
                            f' Note: `typing.Generic` must go last: `class {cls.__name__}({bases_str}): ...`)'
                        )
                    raise TypeError(error_message)

                cls.__pydantic_generic_metadata__ = {
                    'origin': None,
                    'args': (),
                    'parameters': parameters,
                }

            cls.__pydantic_complete__ = False  # Ensure this specific class gets completed

            # preserve `__set_name__` protocol defined in https://peps.python.org/pep-0487
            # for attributes not in `new_namespace` (e.g. private attributes)
            for name, obj in private_attributes.items():
                obj.__set_name__(cls, name)

            if __pydantic_reset_parent_namespace__:
                cls.__pydantic_parent_namespace__ = build_lenient_weakvaluedict(parent_frame_namespace())
            parent_namespace = getattr(cls, '__pydantic_parent_namespace__', None)
            if isinstance(parent_namespace, dict):
                parent_namespace = unpack_lenient_weakvaluedict(parent_namespace)

            types_namespace = get_cls_types_namespace(cls, parent_namespace)
            set_model_fields(cls, bases, config_wrapper, types_namespace)
            complete_model_class(
                cls,
                cls_name,
                config_wrapper,
                raise_errors=False,
                types_namespace=types_namespace,
            )
            # using super(cls, cls) on the next line ensures we only call the parent class's __pydantic_init_subclass__
            # I believe the `type: ignore` is only necessary because mypy doesn't realize that this code branch is
            # only hit for _proper_ subclasses of BaseModel
            super(cls, cls).__pydantic_init_subclass__(**kwargs)  # type: ignore[misc]
            return cls
        else:
            # this is the BaseModel class itself being created, no logic required
            return super().__new__(mcs, cls_name, bases, namespace, **kwargs)

    ...


def set_model_fields(
    cls: type[DbModel], bases: tuple[type[Any], ...], config_wrapper: ConfigWrapper, types_namespace: dict[str, Any]
) -> None:
    """Collect and set `cls.model_fields` and `cls.__class_vars__`.

    Args:
        cls: BaseModel or dataclass.
        bases: Parents of the class, generally `cls.__bases__`.
        config_wrapper: The config wrapper instance.
        types_namespace: Optional extra namespace to look for types in.
    """
    typevars_map = get_model_typevars_map(cls)
    fields, class_vars = collect_model_fields(cls, bases, config_wrapper, types_namespace, typevars_map=typevars_map)
    cls.model_fields = fields
    cls.__class_vars__.update(class_vars)
    for k in class_vars:
        # Class vars should not be private attributes
        #     We remove them _here_ and not earlier because we rely on inspecting the class to determine its classvars,
        #     but private attributes are determined by inspecting the namespace _prior_ to class creation.
        #     In the case that a classvar with a leading-'_' is defined via a ForwardRef (e.g., when using
        #     `__future__.annotations`), we want to remove the private attribute which was detected _before_ we knew it
        #     evaluated to a classvar

        value = cls.__private_attributes__.pop(k, None)
        if value is not None and value.default is not PydanticUndefined:
            setattr(cls, k, value.default)


def collect_model_fields(  # noqa: C901
    cls: type[BaseModel],
    bases: tuple[type[Any], ...],
    config_wrapper: ConfigWrapper,
    types_namespace: dict[str, Any] | None,
    *,
    typevars_map: dict[Any, Any] | None = None,
) -> tuple[dict[str, FieldInfo], set[str]]:
    """Collect the fields of a nascent pydantic model.

    Also collect the names of any ClassVars present in the type hints.

    The returned value is a tuple of two items: the fields dict, and the set of ClassVar names.

    Args:
        cls: BaseModel or dataclass.
        bases: Parents of the class, generally `cls.__bases__`.
        config_wrapper: The config wrapper instance.
        types_namespace: Optional extra namespace to look for types in.
        typevars_map: A dictionary mapping type variables to their concrete types.

    Returns:
        A tuple contains fields and class variables.

    Raises:
        NameError:
            - If there is a conflict between a field name and protected namespaces.
            - If there is a field other than `root` in `RootModel`.
            - If a field shadows an attribute in the parent model.
    """
    from pydantic.fields import FieldInfo

    type_hints = get_cls_type_hints_lenient(cls, types_namespace)

    # https://docs.python.org/3/howto/annotations.html#accessing-the-annotations-dict-of-an-object-in-python-3-9-and-older
    # annotations is only used for finding fields in parent classes
    annotations = cls.__dict__.get('__annotations__', {})
    fields: dict[str, FieldInfo] = {}
    class_vars: set[str] = set()
    for ann_name, ann_type in type_hints.items():
        if ann_name == 'model_config':
            # We never want to treat `model_config` as a field
            # Note: we may need to change this logic if/when we introduce a `BareModel` class with no
            # protected namespaces (where `model_config` might be allowed as a field name)
            continue
        for protected_namespace in config_wrapper.protected_namespaces:
            if ann_name.startswith(protected_namespace):
                for b in bases:
                    if hasattr(b, ann_name):
                        from .main import BaseModel

                        if not (issubclass(b, BaseModel) and ann_name in b.model_fields):
                            raise NameError(
                                f'Field "{ann_name}" conflicts with member {getattr(b, ann_name)}'
                                f' of protected namespace "{protected_namespace}".'
                            )
                else:
                    valid_namespaces = tuple(
                        x for x in config_wrapper.protected_namespaces if not ann_name.startswith(x)
                    )
                    warnings.warn(
                        f'Field "{ann_name}" has conflict with protected namespace "{protected_namespace}".'
                        '\n\nYou may be able to resolve this warning by setting'
                        f" `model_config['protected_namespaces'] = {valid_namespaces}`.",
                        UserWarning,
                    )
        if is_classvar(ann_type):
            class_vars.add(ann_name)
            continue
        if _is_finalvar_with_default_val(ann_type, getattr(cls, ann_name, PydanticUndefined)):
            class_vars.add(ann_name)
            continue
        if not is_valid_field_name(ann_name):
            continue
        if cls.__pydantic_root_model__ and ann_name != 'root':
            raise NameError(
                f"Unexpected field with name {ann_name!r}; only 'root' is allowed as a field of a `RootModel`"
            )

        # when building a generic model with `MyModel[int]`, the generic_origin check makes sure we don't get
        # "... shadows an attribute" errors
        generic_origin = getattr(cls, '__pydantic_generic_metadata__', {}).get('origin')
        is_inheritance = False
        for base in bases:
            if hasattr(base, ann_name):
                if base is generic_origin:
                    # Don't error when "shadowing" of attributes in parametrized generics
                    continue
                # warnings.warn(
                #     f'Field name "{ann_name}" shadows an attribute in parent "{base.__qualname__}"; ',
                #     UserWarning,
                # )
                fields[ann_name] = base.model_fields[ann_name]
                is_inheritance = True
        if is_inheritance:
            continue
        try:
            default = getattr(cls, ann_name, PydanticUndefined)
            if default is PydanticUndefined:
                raise AttributeError
        except AttributeError:
            if ann_name in annotations:
                field_info = FieldInfo.from_annotation(ann_type)
            else:
                # if field has no default value and is not in __annotations__ this means that it is
                # defined in a base class and we can take it from there
                model_fields_lookup: dict[str, FieldInfo] = {}
                for x in cls.__bases__[::-1]:
                    model_fields_lookup.update(getattr(x, 'model_fields', {}))
                if ann_name in model_fields_lookup:
                    # The field was present on one of the (possibly multiple) base classes
                    # copy the field to make sure typevar substitutions don't cause issues with the base classes
                    field_info = copy(model_fields_lookup[ann_name])
                else:
                    # The field was not found on any base classes; this seems to be caused by fields not getting
                    # generated thanks to models not being fully defined while initializing recursive models.
                    # Nothing stops us from just creating a new FieldInfo for this type hint, so we do this.
                    field_info = FieldInfo.from_annotation(ann_type)
        else:
            field_info = FieldInfo.from_annotated_attribute(ann_type, default)
            # attributes which are fields are removed from the class namespace:
            # 1. To match the behaviour of annotation-only fields
            # 2. To avoid false positives in the NameError check above
            try:
                delattr(cls, ann_name)
            except AttributeError:
                pass  # indicates the attribute was on a parent class
        fields[ann_name] = field_info

    if typevars_map:
        for field in fields.values():
            field.apply_typevars_map(typevars_map, types_namespace)

    return fields, class_vars
