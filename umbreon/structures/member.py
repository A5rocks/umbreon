from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from dateutil.parser import isoparse

from .base import DataModelMixin, optional
from .snowflake import Snowflake
from .user import User

if TYPE_CHECKING:
    from .role import Role  # noqa


class Member(DataModelMixin):
    __slots__ = ('user', 'nick', 'roles', 'joined_at',
                 'premium_since', 'deaf', 'mute', 'hoisted_role_id')

    user: User
    nick: str
    roles: List[Snowflake]
    joined_at: datetime
    premium_since: Optional[datetime]
    deaf: bool
    mute: bool
    hoisted_role_id: Optional[Snowflake]

    factories = {
        'joined_at': isoparse,
        'premium_since': optional(isoparse)  # type: ignore
    }

    mapping = {
        'hoisted_role': 'hoisted_role_id'
    }

    @property
    def hoisted_role(self) -> Optional['Role']:
        if self.hoisted_role_id:
            return self.client.cache.get(self.hoisted_role_id)  # type: ignore

        return None
