from .http import HTTPMethod
from enum import IntEnum, auto

API_BASE = 'https://discordapp.com/api/v7'


class SentDataType(IntEnum):
    JSON = auto()
    FILE = auto()
    QUERY = auto()


class ExternalException(UserWarning):
    pass


class RouteData:
    __slots__ = ('hash', 'method', 'route',
                 'datatype', 'resets_in_complete')
    hash: str
    method: HTTPMethod
    route: str
    datatype: SentDataType
    #: Sometimes, you bump into an already used ratelimit.
    #: We have this to track that our "refresh" time is correct.
    resets_in_complete: bool

    def __init__(
        self,
        method: HTTPMethod,
        route: str,
        datatype: SentDataType = SentDataType.JSON
    ):
        self.hash = ''
        self.method = method
        self.route = API_BASE + route
        self.datatype = datatype
        self.resets_in_complete = False
