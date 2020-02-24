from typing import Optional

from .base import DataModelMixin
from .snowflake import Snowflake, SnowflakeDependent


class Attachment(DataModelMixin, SnowflakeDependent):
    __slots__ = ('id', 'filename', 'size', 'url',
                 'proxy_url', 'height', 'width')

    id: Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str
    height: Optional[int]
    widget: Optional[int]
