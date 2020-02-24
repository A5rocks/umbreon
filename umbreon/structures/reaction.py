from .base import DataModelMixin
from .emoji import Emoji


class Reaction(DataModelMixin):
    __slots__ = ('count', 'me', 'emoji')

    count: int
    me: bool
    emoji: Emoji
