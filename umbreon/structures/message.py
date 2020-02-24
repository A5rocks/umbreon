import enum
from datetime import datetime
from typing import List, Optional

from dateutil.parser import isoparse

from .attachment import Attachment
from .base import CaseInsensitiveEnumMeta, DataModelMixin, optional
from .channel import ChannelType
from .embed import Embed
from .member import Member
from .reaction import Reaction
from .role import Role
from .snowflake import Snowflake, SnowflakeDependent
from .user import User


class MessageType(enum.IntEnum, metaclass=CaseInsensitiveEnumMeta):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12


class MessageActivityType(enum.IntFlag, metaclass=CaseInsensitiveEnumMeta):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5  # this is so wack


class MessageFlags(enum.IntFlag, metaclass=CaseInsensitiveEnumMeta):
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4


class MentionedUser(User):  # AAAAA SPECIAL CASES
    __slots__ = ('member')
    member: Member


class MentionedChannel(DataModelMixin, SnowflakeDependent):
    __slots__ = ('id', 'guild_id', 'type', 'name')
    id: Snowflake
    guild_id: Snowflake
    type: ChannelType
    name: str


class MessageActivity(DataModelMixin):
    __slots__ = ('type', 'party_id')
    type: MessageActivityType
    party_id: str  # ... some rich presence thing...


class MessageApplication(DataModelMixin, SnowflakeDependent):
    __slots__ = ('id', 'cover_image', 'description', 'icon', 'name')
    id: Snowflake
    cover_image: str  # TODO: Images
    description: str
    icon: Optional[str]
    name: str


class MessageReference(DataModelMixin):
    __slots__ = ('message_id', 'channel_id', 'guild_id')
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: Snowflake


class Message(DataModelMixin, SnowflakeDependent):
    __slots__ = ('id', 'channel_id', 'guild_id', 'author', 'member',
                 'content', 'timestamp', 'edited_timestamp', 'tts',
                 'mention_everyone', 'mentions', 'mention_roles',
                 'mention_roles', 'mention_channels', 'attachments',
                 'embeds', 'reactions', 'nonce', 'pinned', 'webhook_id',
                 'type', 'activity', 'application',
                 'message_reference', 'flags')

    id: Snowflake
    channel_id: Snowflake
    guild_id: Snowflake
    author: User
    member: Member
    content: str
    timestamp: datetime
    edited_timestamp: Optional[datetime]
    tts: bool
    mention_everyone: bool
    mentions: List[MentionedUser]
    mention_roles: List[Role]
    mention_channels: List[MentionedChannel]
    attachments: List[Attachment]
    embeds: List[Embed]
    reactions: List[Reaction]
    nonce: str  # This may be a Snowflake?
    pinned: bool
    webhook_id: Snowflake
    type: MessageType
    activity: MessageActivity
    application: MessageApplication
    message_reference: MessageReference
    flags: MessageFlags

    factories = {
        'timestamp': isoparse,
        'edited_timestamp': optional(isoparse)  # type: ignore # ??? mypy
    }

    @property
    def channel(self):
        return self.client.cache.get(self.channel_id or 0)
