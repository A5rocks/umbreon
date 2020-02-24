from trio_websocket import (connect_websocket_url,  # type: ignore
                            WebSocketConnection)
from typing import (List, Dict, Callable, Any,
                    Coroutine, Optional, TYPE_CHECKING, TypeVar)
from trio import Nursery, sleep
import json
from zlib import decompressobj
from .gateway_state_machine import GatewayStateMachine
from ..http_base.http_client import HTTPClient

T = TypeVar('T')

try:
    import erlpack  # type: ignore
except ImportError:
    class erlpack:  # type: ignore
        @staticmethod
        def unpack(data: str) -> Any:
            return data

        @staticmethod
        def pack(data: Any) -> str:
            return str(data)

if TYPE_CHECKING:
    from .. import Client

DISPATCHER_TYPE = Callable[
    ['Client', Dict[str, Any]],
    Coroutine[Any, Any, Any]
]


class GatewayConnection:
    token: str
    dispatchers: Dict[str, List[DISPATCHER_TYPE]]
    url: str
    state: GatewayStateMachine
    ws: Optional[WebSocketConnection]
    http: HTTPClient
    buffer: bytearray
    compressed: bool

    def __init__(
        self,
        token: str,
        nursery: Nursery,
        client: 'Client',
        dispatchers: Optional[Dict[str, List[DISPATCHER_TYPE]]] = None,
        url: str = 'wss://gateway.discord.gg/',  # TODO!
        version: int = 6,
        compress: bool = True,
        encoding: str = 'json'
    ):
        if encoding not in ['json', 'etf']:
            raise UserWarning('encoding should be either `json` or `etf`.')
        self.encoding = encoding
        self.token = token
        self.dispatchers = dispatchers or {}
        self.nursery = nursery
        self.ws = None
        self.url = f'{url}?encoding={encoding}&v={version}'
        self.http = client.http
        self.buffer = bytearray()
        self.compress = compress
        self.inflator = decompressobj()

        if self.compress:
            self.url += '&compress=zlib-stream'

        self.state = GatewayStateMachine.connect(
            client,
            nursery,
            self.dispatchers
        )

    async def connect(self) -> None:
        self.ws = await connect_websocket_url(
            self.nursery,
            self.url,
            message_queue_size=5
        )

        self.nursery.start_soon(self.listener)
        self.nursery.start_soon(self.heartbeater)

    async def listener(self) -> None:
        while self.ws is None:
            await sleep(0)

        # lets get this party started!
        await self.ws.send_message(self.encode({
            'op': 2,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': 'Copland',
                    '$browser': 'umbreon',
                    '$device': 'Navi'
                }
            },
        }))

        while True:
            data = await self.ws.get_message()

            # decompress data
            if self.compress:
                self.buffer.extend(data)
                if len(data) < 4 or data[-4:] != b'\x00\x00\xff\xff':
                    return

                data = self.inflator.decompress(self.buffer)
                self.buffer.clear()

            decoded = self.decode(data)

            await self.state.process(decoded)

    async def heartbeater(self) -> None:
        # TODO: handle disconnect... probably just ignore lmao
        while self.ws is None:
            await sleep(0)

        while True:
            await self.ws.send_message(self.state.heartbeat_payload)
            await sleep(self.state.heartbeat_interval)

    def decode(self, data: bytes) -> Dict[str, Any]:
        if self.encoding == 'json':
            return json.loads(data)
        elif self.encoding == 'etf':
            return erlpack.unpack(data)

        return {}

    def encode(self, data: Dict[str, Any]) -> str:
        if self.encoding == 'json':
            return json.dumps(data)
        elif self.encoding == 'etf':
            return erlpack.pack(data)

        return ''
