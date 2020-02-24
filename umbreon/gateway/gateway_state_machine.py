from json import dumps
from typing import (List, Dict, Callable, Any, Optional,
                    Tuple, Coroutine, TYPE_CHECKING)
from trio import current_time, Nursery, sleep
from enum import IntEnum, auto

from .conversion_table import conversion_table
from ..structures.base import DataModelMixin

if TYPE_CHECKING:
    from .. import Client


class GatewayError(Exception):
    pass


class GatewayCode(IntEnum):
    #: send a str to the websocket
    SEND = auto()
    #: kill the connection and then use reconnect logic
    RECONNECT = auto()
    #: kill the connection and then use initial connection logic
    DROP_AND_CONNECT = auto()
    #: just do nothing
    NOTHING = auto()


DISPATCHER_TYPE = Callable[
    ['Client', Dict[str, Any]],
    Coroutine[Any, Any, Any]
]


class GatewayStateMachine:
    dispatchers: Dict[str, List[DISPATCHER_TYPE]]
    seq: Optional[int]
    _last_heartbeat: float
    heartbeat_interval: float
    latency: Optional[float]
    nursery: Nursery
    session_id: str
    client: 'Client'

    @staticmethod
    def encode(data: Dict[str, Any]) -> str:
        return dumps(data)

    @staticmethod
    def frame(opcode: int, data: Any) -> Dict[str, Any]:
        return {'op': opcode, 'd': data}

    @property
    def heartbeat_payload(self) -> str:
        self._last_heartbeat = current_time()

        return self.encode(self.frame(1, self.seq))

    async def process(self, data: Dict[str, Any]) -> Tuple[GatewayCode, Any]:
        # TODO: (De)Compression logic
        received_payload = data

        opcode = received_payload.get('op')

        # as standard in trio:
        await sleep(0)

        if opcode is None:
            raise GatewayError(
                'One of Discord\'s payloads lacked an opcode...'
            )

        if opcode == 0:
            # update internal variables
            self.seq = received_payload.get('s') or self.seq

            dispatch_type = received_payload.get('t', 'WEIRD')
            dispatch_data = received_payload.get('d')

            await self.dispatch(
                dispatch_type,
                dispatch_data)

            if dispatch_type == 'READY':
                self.session_id = (dispatch_data or {}).get('session_id', '')

            return (GatewayCode.NOTHING, None)

        elif opcode == 1:
            return (GatewayCode.SEND, self.heartbeat_payload)

        elif opcode == 7:
            # uh oh... GatewayCode.reconnection time
            # TODO: implement GatewayCode.reconnection
            return (GatewayCode.RECONNECT, self.session_id)

        elif opcode == 9:
            # uh oh... something's wrong
            if received_payload.get('d', False):
                return (GatewayCode.RECONNECT, self.session_id)
            else:
                return (GatewayCode.DROP_AND_CONNECT, None)

        elif opcode == 10:
            # update internal variables
            self.parse_hello(received_payload.get('d', {}))
            return (GatewayCode.NOTHING, None)

        elif opcode == 11:
            if self._last_heartbeat:
                self.latency = current_time() - self._last_heartbeat
                self._last_heartbeat = 0.0
            return (GatewayCode.NOTHING, None)

        raise GatewayError(
            'Discord should not send an operation who\'s opcode is not:\n'
            '0, 1, 7, 9, 10, or 11...\n'
            f'But it just sent opcode {opcode!r}!'
        )

    def parse_hello(self, data: Dict[str, Any]) -> None:
        self.heartbeat_interval = data.get('heartbeat_interval', 42500) / 1000

    async def parse_ready(self, data: Dict[str, Any]) -> None:
        self.session_id = data.get('session_id', '')

        await sleep(0)

    async def dispatch(self, event: str, data: Any) -> None:
        coros: List[DISPATCHER_TYPE] = self.dispatchers.get(event, [])

        conversion = conversion_table.get(event)

        if (isinstance(conversion, type)
           and issubclass(conversion, DataModelMixin)):
            data = conversion(self.client, data)  # type: ignore
            data = data.uncache()
        elif isinstance(conversion, type):
            data = conversion(data)
        elif callable(conversion):
            data = conversion(self.client, data)

        for coro in coros:
            self.nursery.start_soon(coro, self.client, data)

    @classmethod
    def connect(
        cls,
        client: 'Client',
        nursery: Nursery,
        dispatchers: Optional[Dict[str, List[DISPATCHER_TYPE]]] = None,
    ) -> 'GatewayStateMachine':
        return_class = cls()

        return_class.client = client
        return_class.nursery = nursery
        return_class.dispatchers = dispatchers or {}
        return_class.seq = None
        return_class._last_heartbeat = 0.0
        return_class.latency = None
        return_class.session_id = ''
        return_class.heartbeat_interval = 42500 / 1000  # a sane default

        return return_class

    @classmethod
    def reconnect(
        cls,
        client: 'Client',
        nursery: Nursery,
        dispatchers: Optional[Dict[str, List[DISPATCHER_TYPE]]] = None,
        session_id: str = ''
    ) -> 'GatewayStateMachine':
        return_class = cls.connect(client, nursery, dispatchers)
        return_class.session_id = session_id

        return return_class
