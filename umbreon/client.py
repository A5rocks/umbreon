"""
A 'Client' class that ties everything together
"""
from .gateway.gateway_connection import GatewayConnection
from .http_base.http_client import HTTPClient
from .cache.dict_cache import DictCache
from typing import Optional, List, Callable, Coroutine, Dict, Any

from trio import Nursery, open_nursery

DISPATCH_FUNCTION_TYPE = Callable[
    ['Client', Dict[str, Any]],
    Coroutine[Any, Any, Any]
]


class Client:
    http: HTTPClient
    gate: Optional[GatewayConnection]
    dispatchers: Dict[str, List[DISPATCH_FUNCTION_TYPE]]
    cache: DictCache
    _token: str

    def __init__(self, token: str, **kwargs):
        self._token = token
        self.http = HTTPClient(self._token, **kwargs)
        self.dispatchers = {}
        self.cache = DictCache()

    async def start_gateway(
            self,
            nursery: Optional[Nursery] = None, **kwargs
    ) -> None:
        # create an internal nursery if none is passed in.
        if nursery is not None:
            self.gate = GatewayConnection(
                self._token,
                nursery,
                self,
                self.dispatchers,
                **kwargs
            )

            return await self.gate.connect()
        else:
            async with open_nursery() as internal_nursery:
                self.gate = GatewayConnection(
                    self._token,
                    internal_nursery,
                    self,
                    self.dispatchers
                )

                return await self.gate.connect()

    def on_dispatch(self,
                    dispatch_type: str
                    ) -> Callable[[DISPATCH_FUNCTION_TYPE],
                                  DISPATCH_FUNCTION_TYPE]:

        def decoration(function: DISPATCH_FUNCTION_TYPE
                       ) -> DISPATCH_FUNCTION_TYPE:

            if self.dispatchers.get(dispatch_type) is None:
                self.dispatchers[dispatch_type] = []

            self.dispatchers[dispatch_type].append(function)

            return function

        return decoration
