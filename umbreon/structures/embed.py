from datetime import datetime
from json import dumps  # TODO: autoselection between ujson, json
from typing import List

from dateutil.parser import isoparse

from .base import DataModelMixin


class EmbedAuthor(DataModelMixin):
    __slots__ = ('name', 'url', 'icon_url', 'proxy_icon_url')
    name: str
    url: str
    icon_url: str
    proxy_icon_url: str


class EmbedFooter(DataModelMixin):
    __slots__ = ('text', 'icon_url', 'proxy_icon_url')
    text: str
    icon_url: str
    proxy_icon_url: str


class EmbedField(DataModelMixin):
    __slots__ = ('name', 'value', 'inline')
    name: str
    value: str
    inline: bool


class EmbedProvider(DataModelMixin):
    __slots__ = ('name', 'url')
    name: str
    url: str


class EmbedImage(DataModelMixin):
    __slots__ = ('url', 'proxy_url', 'height', 'width')
    url: str
    proxy_url: str
    height: int
    width: int


class EmbedVideo(DataModelMixin):
    __slots__ = ('url', 'height', 'width')
    url: str
    height: int
    width: int


class EmbedThumbnail(DataModelMixin):
    __slots__ = ('url', 'proxy_url', 'height', 'width')
    url: str
    proxy_url: str
    height: int
    width: int


class Embed(DataModelMixin):
    __slots__ = ('title', 'type', 'description', 'url',
                 'timestamp', 'color', 'footer', 'image',
                 'thumbnail', 'video', 'provider', 'author', 'fields')

    title: str
    type: str
    description: str
    url: str
    timestamp: datetime
    color: int  # TODO: Color
    footer: EmbedFooter
    image: EmbedImage
    thumbnail: EmbedThumbnail
    video: EmbedVideo
    provider: EmbedProvider
    author: EmbedAuthor
    fields: List[EmbedField]

    factories = {
        'timestamp': isoparse
    }

    def validate(self) -> bool:
        if (len(self.title) > 256
                or len(self.description) > 2048
                or len(self.fields) > 25
                or max([len(field.name) for field in self.fields]) > 256
                or max([len(field.value) for field in self.fields]) > 1024
                or len(self.footer.text) > 2048
                or len(self.author.name) > 256
                or len(dumps(self.as_dict())) > 6000):
            return False

        return True
