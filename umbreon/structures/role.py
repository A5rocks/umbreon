from .base import DataModelMixin
from .permission import Permissions
from .snowflake import Snowflake, SnowflakeDependent


class Role(DataModelMixin, SnowflakeDependent):
    __slots__ = ('id', 'name', 'color', 'hoist', 'position',
                 'permissions', 'managed', 'mentionable')

    id: Snowflake
    name: str
    color: int  # TODO: Color
    hoist: bool
    position: int
    permissions: Permissions
    managed: bool
    mentionable: bool
