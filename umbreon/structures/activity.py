from enum import IntEnum, IntFlag
from typing import List, Optional

from .base import CaseInsensitiveEnumMeta, DataModelMixin
from .snowflake import Snowflake


class ActivityTimestamps(DataModelMixin):
    __slots__ = ('start', 'end')
    start: int
    end: int


class ActivityEmoji(DataModelMixin):
    __slots__ = ('name', 'id', 'animated')
    name: str
    id: Snowflake
    animated: bool


class ActivityParty(DataModelMixin):
    __slots__ = ('id', 'size')
    id: str
    size: List[int]

    @property
    def current_size(self) -> int:
        return self.size[0]

    @property
    def max_size(self) -> int:
        return self.size[1]


class ActivityAssets(DataModelMixin):
    __slots__ = ('large_image', 'large_text', 'small_image', 'small_text')
    large_image: str
    large_text: str
    small_image: str
    small_text: str


class ActivitySecrets(DataModelMixin):
    __slots__ = ('join', 'spectate', 'match')
    join: str
    spectate: str
    match: str


class ActivityType(IntEnum, metaclass=CaseInsensitiveEnumMeta):
    GAME = 0
    STREAM = 1
    SONG = 2
    CUSTOM = 4


class ActivityFlags(IntFlag, metaclass=CaseInsensitiveEnumMeta):
    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5


class Activity(DataModelMixin):
    __slots__ = ('name', 'type', 'url', 'created_at', 'timestamps',
                 'application_id', 'details', 'state', 'emoji',
                 'party', 'assets', 'secrets', 'instance', 'flags')

    name: str
    type: ActivityType
    url: Optional[str]
    created_at: int
    timestamps: ActivityTimestamps
    application_id: Snowflake
    details: Optional[str]
    state: Optional[str]
    emoji: Optional[ActivityEmoji]
    party: ActivityParty
    assets: ActivityAssets
    secrets: ActivitySecrets
    instance: bool
    flags: ActivityFlags
