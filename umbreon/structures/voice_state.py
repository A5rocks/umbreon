from typing import Optional

from .base import DataModelMixin
from .member import Member
from .snowflake import Snowflake


class VoiceState(DataModelMixin):
    __slots__ = ('guild_id', 'channel_id', 'user_id', 'member',
                 'session_id', 'deaf', 'mute', 'self_deaf',
                 'self_mute', 'self_stream', 'suppress')

    guild_id: Snowflake
    channel_id: Optional[Snowflake]
    user_id: Snowflake
    member: Member
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: bool
    suppress: bool
