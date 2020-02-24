from typing import Any

from .base import IDDependent


class Snowflake(IDDependent):
    __slots__ = ('id')

    id: int

    def __init__(self, id: int):
        self.id = int(id) if id else 0

    def __str__(self) -> str:
        return str(self.id)

    def __int__(self) -> int:
        return int(self.id)


class SnowflakeDependent:
    """Nice default dunder methods for objects with unique snowflakes."""
    __slots__ = ()
    id: Snowflake = Snowflake(0)  # default id in case none is found.

    def __hash__(self) -> int:
        """Decrease size of sets"""
        return self.id.id

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SnowflakeDependent):
            return (self.id == other.id) if hasattr(other, 'id') else False
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return '[%s#%d]' % (self.__class__.__name__, self.id.id)
