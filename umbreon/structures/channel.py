from datetime import datetime
from enum import Enum, IntEnum
from json import loads
from typing import List, Optional

from dateutil.parser import isoparse

from .base import CaseInsensitiveEnumMeta, DataModelMixin
from .permission import Permissions
from .snowflake import Snowflake, SnowflakeDependent
from .user import User

from ..http_base.routing_table import RoutingTable


class ChannelType(IntEnum, metaclass=CaseInsensitiveEnumMeta):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6


class PermissionOverwriteType(Enum, metaclass=CaseInsensitiveEnumMeta):
    ROLE = 'role'
    MEMBER = 'member'


class PermissionOverwrite(DataModelMixin):
    __slots__ = ('id', 'type', 'allow', 'deny')

    id: Snowflake
    type: str  # either role or member
    allow: Permissions
    deny: Permissions


class Channel(DataModelMixin, SnowflakeDependent):
    __slots__ = ('id', 'type', 'guild_id', 'position',
                 'permission_overwrites', 'name', 'topic',
                 'nsfw', 'last_message_id', 'bitrate', 'user_limit',
                 'rate_limit_per_user', 'recipients', 'icon', 'owner_id',
                 'application_id', 'parent_id', 'last_pin_timestamp')

    id: Snowflake
    type: ChannelType
    guild_id: Snowflake
    position: int
    permission_overwrites: List[PermissionOverwrite]
    name: str
    topic: Optional[str]
    nsfw: bool
    last_message_id: Optional[Snowflake]
    bitrate: int
    user_limit: int
    rate_limit_per_user: int
    recipients: List[User]
    icon: Optional[str]
    owner_id: Snowflake
    application_id: Snowflake
    parent_id: Optional[Snowflake]
    last_pin_timestamp: datetime

    factories = {
        'last_pin_timestamp': isoparse
    }

    async def fill(self) -> Optional['Channel']:
        result = await self.client.http.request(
            RoutingTable.get_channel,
            channel_id=self.id
        )

        if result.status_code != 200:
            return None  # TODO: ?

        result = Channel(loads(result))

        self.client.cache.pass_through(result)

        return result

    async def modify(self):
        result = await self.client.http.request(
            RoutingTable.modify_channel,
            self.asdict(),
            channel_id=self.id
        )

        if result.status_code != 200:
            return None  # TODO: ?

        result = Channel(loads(result))

        self.client.cache.pass_through(result)

        return result
