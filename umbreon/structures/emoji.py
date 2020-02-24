from typing import List, Optional

from .base import DataModelMixin
from .snowflake import Snowflake
from .user import User


class Emoji(DataModelMixin):
    __slots__ = ('id', 'name', 'roles', 'user',
                 'require_colons', 'managed', 'animiated')

    id: Optional[Snowflake]  # ... okay then? only for custom emojis
    name: Optional[str]  # if this is nulled, its a reaction + custom
    roles: List[Snowflake]
    user: User
    require_colons: bool
    managed: bool
    animated: bool

    @property
    def representation(self) -> str:
        return self.name or str(self.id)

    def __hash__(self) -> int:
        return hash(self.representation)
