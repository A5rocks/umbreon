"""
Not a good implementation of a ratelimiter,
but at this point I just need to get an alpha
out. Contributions very welcomed, even if you
replace this whole file! Even if the api to
use changes, anything is better than *this*.
"""

import trio

from typing import Optional, Tuple, Dict


class Container:
    __slots__ = ('_uses', 'last_use', 'sleepers')
    _uses: int
    last_use: float
    sleepers: int

    def __init__(self, uses: int = 1):
        self._uses = uses
        self.sleepers = 0

        if uses > 0:
            self.last_use = trio.current_time()
        else:
            self.last_use = 0

    @property
    def uses(self) -> int:
        return self._uses

    @uses.setter
    def uses(self, value: int) -> None:
        if self.uses <= 0 and value > 0:
            self.last_use = trio.current_time()

        self._uses = value

    def reset(self, to: int = 1) -> None:
        self.uses = to
        self.last_use = trio.current_time()


class Ratelimit:
    __slots__ = ('limit', 'refresh', 'containers', 'cushion')
    limit: int
    refresh: int
    #: Because networks are totally reliable :tm:
    cushion: float
    #: The tuple should be (user_id, channel_id, guild_id), but
    #: if a field is not present the tuple should not contain it.
    containers: Dict[Tuple[int, ...], Container]

    def __init__(self,
                 limit: int = 1,
                 refresh: int = 0,
                 initial_request: Optional[Tuple[int, ...]] = None,
                 initial_requests: int = 1,
                 cushion: float = 0.1):
        self.limit = limit
        self.refresh = refresh
        self.cushion = cushion

        if not initial_request:
            self.containers = {}
        else:
            self.containers = {initial_request: Container(initial_requests)}

    async def acquire(self, request: Optional[Tuple[int, ...]] = None) -> None:
        if request is None:
            request = ()

        if request not in self.containers:
            self.containers[request] = Container(0)

        self.containers[request].uses += 1

        if self.containers[request].uses > self.limit:
            await trio.sleep_until(
                self.containers[request].last_use + self.refresh + self.cushion
            )

            self.containers[request].reset()

        # keep with trio conventions
        await trio.sleep(0)
