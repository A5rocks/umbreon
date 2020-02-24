from enum import Enum


class HTTPMethod(Enum):
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    HEAD = 'HEAD'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
