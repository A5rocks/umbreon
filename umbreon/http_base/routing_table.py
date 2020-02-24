from .route import RouteData as Route
from .http import HTTPMethod as h
from .route import SentDataType as f

from typing import Any, Dict


class InsensitiveMeta(type):
    def __new__(cls,
                name: str,
                bases: Any,
                attrs: Dict[str, Any]) -> Any:
        attrs = {k.lower(): v for k, v in attrs.items()}

        attrs.update(
            {'__getattr__': lambda self, name: getattr(self, name.lower())}
        )

        return super(InsensitiveMeta, cls).__new__(cls, name, bases, attrs)

    def __getattr__(cls, name: str) -> Any:
        if name.islower():
            return None
        return getattr(cls, name.lower())


class RoutingMeta(InsensitiveMeta):
    def __new__(cls,
                name: str,
                bases: Any,
                attrs: Dict[str, Any]) -> Any:

        attrs = {
            k: Route(*v) if k and k[0] != '_' else v for k, v in attrs.items()
        }

        return super(RoutingMeta, cls).__new__(cls, name, bases, attrs)


# stupid line limits...
CHANNEL_BASE = '/channels/{channel_id}'
REACTION_BASE = CHANNEL_BASE + '/messages/{message_id}/reactions/{emoji}'
CHANNEL_PERMS_BASE = CHANNEL_BASE + '/permissions/{overwrite_id}'
GUILD_MEMBER_BASE = '/guilds/{guild_id}/members/{user_id}'
GUILD_INTEGRATION = '/guilds/{guild_id}/integrations/{integration_id}'


class RoutingTable(metaclass=RoutingMeta):
    # channel routes
    get_channel = h.GET, CHANNEL_BASE
    modify_channel = h.PATCH, CHANNEL_BASE
    delete_channel = h.DELETE, CHANNEL_BASE
    get_pins = h.GET, CHANNEL_BASE + '/pins'
    get_reactions = h.GET, REACTION_BASE, f.QUERY
    delete_all_reactions = h.DELETE, REACTION_BASE
    edit_channel_perms = h.PUT, CHANNEL_PERMS_BASE
    create_reaction = h.PUT, REACTION_BASE + '/@me'
    trigger_typing = h.POST, CHANNEL_BASE + '/typing'
    trigger_typing = h.POST, CHANNEL_BASE + '/typing'
    add_pin = h.PUT, CHANNEL_BASE + '/pins/{message_id}'
    get_channel_invites = h.GET, CHANNEL_BASE + '/invites'
    delete_self_reaction = h.DELETE, REACTION_BASE + '/@me'
    delete_channel_permission = h.DELETE, CHANNEL_PERMS_BASE
    create_channel_invite = h.POST, CHANNEL_BASE + '/invites'
    create_message = h.POST, CHANNEL_BASE + '/messages', f.FILE
    delete_pin = h.DELETE, CHANNEL_BASE + '/pins/{message_id}'
    bulk_delete = h.POST, CHANNEL_BASE + '/messages/bulk-delete'
    group_dm_add = h.PUT, CHANNEL_BASE + '/recipients/{user_id}'
    delete_user_reaction = h.DELETE, REACTION_BASE + '/{user_id}'
    edit_message = h.PATCH, CHANNEL_BASE + '/messages/{message_id}'
    get_channel_messages = h.GET, CHANNEL_BASE + '/messages', f.QUERY
    delete_message = h.DELETE, CHANNEL_BASE + '/messages/{message_id}'
    group_dm_remove = h.DELETE, CHANNEL_BASE + '/recipients/{user_id}'
    get_channel_message = h.GET, CHANNEL_BASE + '/messages/{message_id}'

    # emoji routes
    get_guild_emojis = h.GET, '/guilds/{guild_id}/emojis'
    create_guild_emoji = h.POST, '/guilds/{guild_id}/emojis'
    get_guild_emoji = h.GET, '/guilds/{guild_id}/emojis/{emoji_id}'
    modify_guild_emoji = h.PATCH, '/guilds/{guild_id}/emojis/{emoji_id}'
    delete_guild_emoji = h.DELETE, '/guilds/{guild_id}/emojis/{emoji_id}'

    # guild routes
    create_guild = h.POST, '/guilds'
    get_guild = h.GET, '/guilds/{guild_id}'
    kick_member = h.DELETE, GUILD_MEMBER_BASE
    add_guild_member = h.PUT, GUILD_MEMBER_BASE
    get_bans = h.GET, '/guilds/{guild_id}/bans'
    get_guild_member = h.GET, GUILD_MEMBER_BASE
    modify_guild = h.PATCH, '/guilds/{guild_id}'
    delete_guild = h.DELETE, '/guilds/{guild_id}'
    get_roles = h.GET, '/guilds/{guild_id}/roles'
    create_role = h.POST, '/guilds/{guild_id}/roles'
    modify_guild_member = h.PATCH, GUILD_MEMBER_BASE
    prune_members = h.POST, '/guilds/{guild_id}/prune'
    get_guild_embed = h.GET, '/guilds/{guild_id}/embed'
    modify_guild_integration = h.PATCH, GUILD_INTEGRATION
    delete_guild_integration = h.DELETE, GUILD_INTEGRATION
    ban_member = h.PUT, '/guilds/{guild_id}/bans/{user_id}'
    get_guild_invites = h.GET, '/guilds/{guild_id}/invites'
    get_vanity_url = h.GET, '/guilds/{guild_id}/vanity-url'
    list_guild_members = h.GET, '/guilds/{guild_id}/members'
    modify_guild_embed = h.PATCH, '/guilds/{guild_id}/embed'
    get_guild_channels = h.GET, '/guilds/{guild_id}/channels'
    prune_members_dryrun = h.GET, '/guilds/{guilds_id}/prune'
    get_guild_ban = h.GET, '/guilds/{guild_id}/bans/{user_id}'
    remove_ban = h.DELETE, '/guilds/{guild_id}/bans/{user_id}'
    modify_role_positions = h.PATCH, '/guilds/{guild_id}/roles'
    create_guild_channel = h.POST, '/guilds/{guild_id}/channels'
    sync_guild_integration = h.POST, GUILD_INTEGRATION + '/sync'
    get_guild_voice_regions = h.GET, '/guilds/{guild_id}/regions'
    get_guild_integrations = h.GET, '/guilds/{guild_id}/integrations'
    modify_channel_positions = h.PATCH, '/guilds/{guild_id}/channels'
    modify_guild_role = h.PATCH, '/guilds/{guild_id}/roles/{role_id}'
    modify_self_nick = h.PATCH, '/guilds/{guild_id}/members/@me/nick'
    delete_guild_role = h.DELETE, '/guilds/{guild_id}/roles/{role_id}'
    get_guild_widget = h.GET, '/guilds/{guild_id}/widget.png', f.QUERY
    add_guild_member_role = h.PUT, GUILD_MEMBER_BASE + '/roles/{role_id}'
    remove_guild_member_role = h.DELETE, GUILD_MEMBER_BASE + '/roles/{role_id}'

    # invite routes
    # TODO: invite object / metadata in structures
    get_invite = h.GET, '/invites/{invite_code}'
    delete_invite = h.DELETE, '/invites/{invite_code}'

    # user routes
    get_self_user = h.GET, '/users/@me'
    get_user = h.GET, '/users/{user_id}'
    modify_self_user = h.PATCH, '/users/@me'
    create_dm = h.POST, '/users/@me/channels'
    get_self_guilds = h.GET, '/users/@me/guilds', f.QUERY
    get_self_connections = h.GET, '/users/@me/connections'
    leave_guild = h.DELETE, '/users/@me/guilds/{guild_id}'
    get_self_dms = h.GET, '/users/@me/channels'  # for bots: = []
    create_group_dm = h.POST, '/users/@me/channels'  # invisible to the client

    # voice routes
    # TODO: voice regions
    list_voice_regions = h.GET, '/voice/regions'

    # webhook routes
    # TODO: webhooks
    get_webhook = h.GET, '/webhooks/{webhook_id}'
    modify_webhook = h.PATCH, '/webhooks/{webhook_id}'
    delete_webhook = h.DELETE, '/webhooks/{webhook_id}'
    get_webhooks = h.GET, '/channels/{channel_id}/webhooks'
    create_webhook = h.POST, '/channels/{channel_id}/webhooks'
    execute_webhook = h.POST, '/webhooks/{webhook_id}/{webhook_token}'
    tokened_get_webhook = h.GET, '/webhooks/{webhook_id}/{webhook_token}'
    slack_webhook = h.POST, '/webhooks/{webhook_id}/{webhook_token}/slack'
    github_webhook = h.POST, '/webhooks/{webhook_id}/{webhook_token}/github'
    tokened_modify_webhook = h.PATCH, '/webhooks/{webhook_id}/{webhook_token}'
    tokened_delete_webhook = h.DELETE, '/webhooks/{webhook_id}/{webhook_token}'

    # audit log routes
    # TODO: Audit Log stuctures
    get_audit_log = h.GET, '/guilds/{guild_id}/audit-logs'
