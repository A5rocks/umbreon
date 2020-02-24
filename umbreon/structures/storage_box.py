from typing import TYPE_CHECKING, Any, Dict, Optional, Union

if TYPE_CHECKING:
    from .base import DataModelMixin


class StorageBox:
    __slots__ = ('_model', '__dict__')
    _model: 'DataModelMixin'

    def __init__(self, model: 'DataModelMixin'):
        self._model = model

    def update(self, dictionary: Union[Dict[str, Any], 'StorageBox']) -> None:
        if isinstance(dictionary, StorageBox):
            self.update(dictionary.as_dict())
            return

        if '_model' in dictionary:
            raise UserWarning('`_model` is reserved storage space.')

        self.__dict__.update(dictionary)

    def as_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def get(self, name: str, default: Optional[Any] = None) -> Any:
        return self.__dict__.get(name, default)

    def __getattr__(self, name: str) -> None:
        return None

    def __bool__(self) -> bool:
        return bool(len(self.__dict__))
