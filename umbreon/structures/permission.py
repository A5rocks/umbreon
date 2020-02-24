import enum

from .base import CaseInsensitiveEnumMeta


class Permissions(enum.IntFlag, metaclass=CaseInsensitiveEnumMeta):
    # kinda just copy pasted from gitlab.com/nekokatt/hikari...
    NONE = 0x0
    CREATE_INSTANT_INVITE = 0x1
    KICK_MEMBERS = 0x2
    BAN_MEMBERS = 0x4
    ADMINISTRATOR = 0x8
    MANAGE_CHANNELS = 0x10
    MANAGE_GUILD = 0x20
    ADD_REACTIONS = 0x40
    VIEW_AUDIT_LOG = 0x80
    PRIORITY_SPEAKER = 0x1_00
    STREAM = 0x2_00
    VIEW_CHANNEL = 0x4_00
    SEND_MESSAGES = 0x8_00
    SEND_TTS_MESSAGES = 0x10_00
    MANAGE_MESSAGES = 0x20_00
    EMBED_LINKS = 0x40_00
    ATTACH_FILES = 0x80_00
    READ_MESSAGE_HISTORY = 0x1_00_00
    MENTION_EVERYONE = 0x2_00_00
    USE_EXTERNAL_EMOJIS = 0x4_00_00
    CONNECT = 0x10_00_00
    SPEAK = 0x20_00_00
    MUTE_MEMBERS = 0x40_00_00
    DEAFEN_MEMBERS = 0x80_00_00
    MOVE_MEMBERS = 0x1_00_00_00
    USE_VAD = 0x2_00_00_00
    CHANGE_NICKNAME = 0x4_00_00_00
    MANAGE_NICKNAMES = 0x8_00_00_00
    MANAGE_ROLES = 0x10_00_00_00
    MANAGE_WEBHOOKS = 0x20_00_00_00
    MANAGE_EMOJIS = 0x40_00_00_00
