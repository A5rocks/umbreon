from ..structures import (Channel, Emoji, Guild, Member, Message,
                          PresenceUpdate, Role, Snowflake,
                          User, VoiceState)
from ..structures.base import optional, DataModelMixin
from functools import partial
from typing import Dict, Any, Callable
from dateutil.parser import isoparse


def converter(schema: Dict[str, Any]) -> Callable:
    # def conversion(client, data: Dict[str, Any]) -> Any:
    def conversion(client, data: Dict[str, Any]) -> Any:

        out_dict = {}
        for key, converter in schema.items():
            if key in data.keys():
                if (isinstance(converter, type)
                   and issubclass(converter, DataModelMixin)):
                    out_dict[key] = converter(client, data[key])
                elif isinstance(converter, type) or callable(converter):
                    out_dict[key] = converter(data[key])  # type: ignore
                # out_dict[key] = converter(data[key])

        return out_dict

    return conversion


def empty_func(*args: Any) -> None:
    ...


conversion_table = {
    'HELLO': {'heartbeat_interval': int},
    'READY': {
        'v': int, 'user': User, 'private_channels': list,
        'guilds': partial(map, Guild), 'session_id': str, 'shard': list},
    'RESUMED': empty_func,
    'RECONNECT': empty_func,
    'INVALID_SESSION': bool,
    'CHANNEL_CREATE': Channel,
    'CHANNEL_UPDATE': Channel,
    'CHANNEL_DELETE': Channel,
    'CHANNEL_PINS_UPDATE': {
        'guild_id': Snowflake, 'channel_id': Snowflake,
        'last_pin_timestamp': isoparse},
    'GUILD_CREATE': Guild,
    'GUILD_UPDATE': Guild,
    'GUILD_DELETE': Guild,
    'GUILD_BAN_ADD': {'guild_id': Snowflake, 'user': User},
    'GUILD_BAN_REMOVE': {'guild_id': Snowflake, 'user': User},
    'GUILD_EMOJIS_UPDATE': {
        'guild_id': Snowflake, 'emojis': partial(map, Emoji)},
    'GUILD_INTEGRATIONS_UPDATE': {'guild_id': Snowflake},
    'GUILD_MEMBER_ADD': Member,  # has an extra field, `guild_id`...
    'GUILD_MEMBER_REMOVE': {'guild_id': Snowflake, 'user': User},
    'GUILD_MEMBER_UPDATE': {
        'guild_id': Snowflake, 'roles': partial(map, Snowflake), 'user': User,
        # frick discord... the only nullable field possible is "premium_since"
        'nick': str, 'premium_since': optional(isoparse)},
    'GUILD_MEMBERS_CHUNK': {
        'guild_id': Snowflake, 'members': partial(map, Member),
        'not_found': list, 'presences': partial(map, PresenceUpdate)},
    'GUILD_ROLE_CREATE': {'guild_id': Snowflake, 'role': Role},
    'GUILD_ROLE_UPDATE': {'guild_id': Snowflake, 'role': Role},
    'GUILD_ROLE_DELETE': {'guild_id': Snowflake, 'role_id': Snowflake},
    'MESSAGE_CREATE': Message,
    'MESSAGE_UPDATE': Message,
    'MESSAGE_DELETE': {
        'id': Snowflake, 'channel_id': Snowflake, 'guild_id': Snowflake},
    'MESSAGE_DELETE_BULK': {
        'ids': partial(map, Snowflake), 'channel_id': Snowflake,
        'guild_id': Snowflake},
    'MESSAGE_REACTION_ADD': {
        'user_id': Snowflake, 'channel_id': Snowflake, 'message_id': Snowflake,
        'guild_id': Snowflake, 'member': Member, 'emoji': Emoji},
    'MESSAGE_REACTION_REMOVE': {
        'user_id': Snowflake, 'channel_id': Snowflake, 'message_id': Snowflake,
        'guild_id': Snowflake, 'emoji': Emoji},
    'MESSAGE_REACTION_REMOVE_ALL': {
        'channel_id': Snowflake, 'message_id': Snowflake,
        'guild_id': Snowflake},
    'PRESENCE_UPDATE': PresenceUpdate,
    'TYPING_START': {
        'channel_id': Snowflake, 'guild_id': Snowflake, 'user_id': Snowflake,
        'timestamp': int, 'member': Member},
    'USER_UPDATE': User,
    'VOICE_STATE_UPDATE': VoiceState,
    'VOICE_SERVER_UPDATE': {
        'token': str, 'guild_id': Snowflake, 'endpoint': str},
    'WEBHOOKS_UPDATE': {'guild_id': Snowflake, 'channel_id': Snowflake}
}

for key, value in conversion_table.items():
    if isinstance(value, dict):
        conversion_table[key] = converter(value)
