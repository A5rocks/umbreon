import enum
import functools
from typing import (Any, Callable, Dict, List, Optional,
                    Set, TypeVar, Union, TYPE_CHECKING)

from .storage_box import StorageBox
from .unset import Unset

if TYPE_CHECKING:
    from .. import Client

T = TypeVar('T')
A = TypeVar('A')


def is_nonetype(arg: Any) -> bool:
    return arg is None


def is_not_nonetype(arg: Any) -> bool:
    return not is_nonetype(arg)


def default_func(arg: T) -> T:
    return arg


class CaseInsensitiveEnumMeta(enum.EnumMeta):
    def __getitem__(self, item: str) -> Any:
        if isinstance(item, str):
            item = item.upper()
        return super(CaseInsensitiveEnumMeta, self).__getitem__(item)


class DataModelMixin:
    __slots__ = ('client', 'storage')
    factories: Dict[str, Callable[[Any], Any]] = {}
    mapping: Dict[str, str] = {}
    undocumented: Set[str] = {'lazy', 'self_video'}
    storage: StorageBox

    def __init__(self,
                 client: 'Client',
                 dictionary: Optional[Dict[str, Any]] = None,
                 **backup_dictionary: Dict[str, Any]):
        self.client = client
        self.storage = StorageBox(self)

        dictionary = dictionary or {}
        dictionary.update(backup_dictionary)

        for attr, value in dictionary.items():
            attr = self.mapping.get(attr, attr)

            if attr not in dir(self.__class__):
                if attr not in self.undocumented:
                    print(
                        f'`{attr}` is not documented '
                        f'in `{self.__class__.__name__}`'
                    )
                    self.undocumented.update({attr})

                continue

            transformer = (self.factories.get(attr)
                           or self.__annotations__.get(attr)
                           or default_func)

            # allow optional variables
            args = []
            is_union = False
            is_list = False

            if hasattr(transformer, '__args__'):
                origin = getattr(transformer, '__origin__', None)
                is_union = origin == Union
                is_list = (origin == list) or (origin == List)
                args = getattr(transformer, '__args__')

            if args is None:
                continue

            seived = filter(is_not_nonetype, args)
            was_optional_dataclass = False
            if is_union and seived and type(None) in args:
                element = list(seived)[0]
                transformer = optional(element)

                if (isinstance(element, type)
                   and issubclass(element, DataModelMixin)):
                    was_optional_dataclass = True

            # allow lists
            was_list_dataclass = False
            if is_list and args:
                if (isinstance(args[0], type)
                   and issubclass(args[0], DataModelMixin)):
                    transformer = functools.partial(args[0], client)
                    transformer = functools.partial(map, transformer)
                    was_list_dataclass = True
                else:
                    transformer = functools.partial(map, args[0])

            # feed client into other dataclasses
            was_dataclass = False
            if (isinstance(transformer, type)
               and issubclass(transformer, DataModelMixin)):
                transformer = functools.partial(transformer, client)
                was_dataclass = True

            transformed_value = transformer(value)  # type: ignore

            if was_dataclass:
                client.cache.pass_through(transformed_value)

            if was_optional_dataclass:
                if transformed_value is not None:
                    client.cache.pass_through(transformed_value)

            if is_list and args:
                transformed_value = list(transformed_value)  # type: ignore
                if was_list_dataclass:
                    list(map(client.cache.pass_through, transformed_value))

            setattr(self, attr, transformed_value)

    def as_dict(self) -> Dict[str, Any]:
        return_dictionary: Dict[str, Any] = {}
        inverse_mapping = {v: k for k, v in self.mapping.items()}

        for key in dir(self):
            if key[:1] == '__':
                continue

            value = getattr(self, key)
            key = inverse_mapping.get(key, key)

            if value is not Unset:
                return_dictionary[key] = value

        return return_dictionary

    def __getattr__(self, attr: str) -> Unset:
        """Decreases the number of accidental errors... Maybe..."""
        return Unset()

    def uncache(self) -> 'DataModelMixin':
        # recursive!
        for attr in self.__slots__:
            if isinstance(getattr(self, attr, None), DataModelMixin):
                setattr(self, attr, getattr(self, attr, None).uncache())

        return self.client.cache.pass_through(self)


class IDDependent:
    """Nice dunder methods for objects with unique IDs."""
    __slots__ = ()
    id: int = 0  # default id in case none is found.

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, IDDependent):
            return (self.id == other.id) if hasattr(other, 'id') else False
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return '%s(%d)' % (self.__class__.__name__, self.id)


def optional(
    function: Callable[[T], A]
) -> Callable[[Optional[T]], Optional[A]]:
    @functools.wraps(function)
    def decoration(argument: Optional[T]) -> Optional[A]:
        return function(argument) if argument else None

    return decoration
