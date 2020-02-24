from datetime import datetime
from typing import List, Optional

from dateutil.parser import isoparse

from .activity import Activity
from .base import DataModelMixin, optional
from .client_status import ClientStatus
from .snowflake import Snowflake
from .user import User


class PresenceUpdate(DataModelMixin):
    __slots__ = ('user', 'roles', 'game', 'guild_id', 'status',
                 'activities', 'client_status', 'premium_since', 'nick')

    user: User
    roles: List[Snowflake]
    game: Optional[Activity]
    guild_id: Snowflake
    status: str
    activities: List[Activity]
    client_status: ClientStatus
    premium_since: Optional[datetime]
    nick: Optional[str]

    factories = {
        'premium_since': optional(isoparse)  # type: ignore
    }
