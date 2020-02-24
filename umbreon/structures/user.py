from enum import IntEnum, IntFlag
from typing import Optional

from .base import CaseInsensitiveEnumMeta, DataModelMixin
from .snowflake import Snowflake, SnowflakeDependent


class UserFlags(IntFlag, metaclass=CaseInsensitiveEnumMeta):
    NONE = 0
    DISCORD_EMPLOYEE = 1 << 0
    DISCORD_PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER = 1 << 3
    HYPESQUAD_BRAVERY = 1 << 6
    HYPESQUAD_BRILLIANCE = 1 << 7
    HYPESQUAD_BALANCE = 1 << 8
    EARLY_SUPPORTER = 1 << 9
    TEAM_USER = 1 << 10
    SYSTEM = 1 << 12


class PremiumType(IntEnum, metaclass=CaseInsensitiveEnumMeta):
    NITRO_CLASSIC = 1
    NITRO = 2


class User(DataModelMixin, SnowflakeDependent):
    __slots__ = ('id', 'username', 'discriminator', 'avatar',
                 'bot', 'system', 'mfa_enabled', 'locale',
                 'verified', 'email', 'flags', 'premium_type')

    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    bot: bool
    system: bool
    mfa_enabled: bool
    locale: str
    verified: bool
    email: str
    flags: UserFlags
    premium_type: PremiumType
