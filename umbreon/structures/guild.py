from datetime import datetime
from enum import Enum, IntEnum, IntFlag
from typing import List, Optional

from dateutil.parser import isoparse

from .base import CaseInsensitiveEnumMeta, DataModelMixin
from .channel import Channel
from .emoji import Emoji
from .member import Member
from .permission import Permissions
from .presence import PresenceUpdate
from .role import Role
from .snowflake import Snowflake, SnowflakeDependent
from .voice_state import VoiceState


class VerificationLevel(IntEnum, metaclass=CaseInsensitiveEnumMeta):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class MessageNotificationLevel(IntEnum, metaclass=CaseInsensitiveEnumMeta):
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class ContentFilter(IntEnum, metaclass=CaseInsensitiveEnumMeta):
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class MFALevel(IntEnum, metaclass=CaseInsensitiveEnumMeta):
    NONE = 0
    ELEVATED = 1


class PremiumTier(IntEnum, metaclass=CaseInsensitiveEnumMeta):
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


class GuildFeatures(Enum, metaclass=CaseInsensitiveEnumMeta):
    INVITE_SPLASH = 'INVITE_SPLASH'
    VIP_REGIONS = 'VIP_REGIONS'
    VANITY_URL = 'VANITY_URL'
    VERIFIED = 'VERIFIED'
    PARTNERED = 'PARTNERED'
    PUBLIC = 'PUBLIC'
    COMMERCE = 'COMMERCE'
    NEWS = 'NEWS'
    DISCOVERABLE = 'DISCOVERABLE'
    FEATURABLE = 'FEATURABLE'
    ANIMATED_ICON = 'ANIMATED_ICON'
    BANNER = 'BANNER'


class SystemChannelFlags(IntFlag, metaclass=CaseInsensitiveEnumMeta):
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_NOTIFICATIONS = 1 << 1  # why?


class Guild(DataModelMixin, SnowflakeDependent):
    __slots__ = ('id', 'name', 'icon', 'splash', 'discovery_splash', 'owner',
                 'owner_id', 'permissions', 'region', 'afk_channel_id',
                 'afk_timeout', 'embed_enabled', 'embed_channel_id',
                 'verification_level', 'default_message_notifications',
                 'explicit_content_filter', 'roles', 'emojis', 'features',
                 'mfa_level', 'application_id', 'widget_enabled',
                 'widget_channel_id', 'system_channel_id',
                 'joined_at', 'large', 'unavailable', 'member_count',
                 'voice_states', 'members', 'channels', 'presences',
                 'max_presences', 'max_members', 'vanity_url_code',
                 'description', 'banner', 'premium_tier',
                 'premium_subscription_count', 'preferred_locale',
                 'rules_channel_id', 'system_channel_flags',
                 'public_updates_channel_id')

    id: Snowflake
    name: str
    icon: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]  # TODO: images
    owner: bool
    owner_id: Snowflake
    permissions: Permissions
    region: str
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    embed_enabled: bool
    embed_channel_id: Snowflake
    verification_level: VerificationLevel
    default_message_notifications: MessageNotificationLevel
    explicit_content_filter: ContentFilter
    roles: List[Role]
    emojis: List[Emoji]
    features: List[GuildFeatures]
    mfa_level: MFALevel
    application_id: Optional[Snowflake]
    widget_enabled: bool
    widget_channel_id: Snowflake
    system_channel_id: Optional[Snowflake]
    joined_at: datetime
    large: bool
    unavailable: bool
    member_count: int
    voice_states: List[VoiceState]
    members: List[Member]
    channels: List[Channel]
    presences: List[PresenceUpdate]
    max_presences: Optional[int]
    max_members: int
    vanity_url_code: Optional[str]
    description: Optional[str]
    banner: Optional[str]  # TODO: Images
    premium_tier: PremiumTier
    premium_subscription_count: int
    preferred_local: str
    rules_channel_id: Snowflake
    system_channel_flags: SystemChannelFlags
    public_updates_channel_id: Optional[Snowflake]

    factories = {
        'joined_at': isoparse
    }
