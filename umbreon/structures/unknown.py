from typing import Any, Dict


class UnknownType:
    """A layman's version of `NotImplementedError`"""
    def __init__(self, dictionary: Dict[str, Any]):
        for attr, value in dictionary.items():
            setattr(self, attr, value)

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Any]) -> 'UnknownType':
        returned_class = cls(dictionary)
        return returned_class
