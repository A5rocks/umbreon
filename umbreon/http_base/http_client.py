from .http import HTTPMethod
from .route import RouteData, SentDataType, ExternalException
from .ratelimit import Ratelimit
from ..structures import Snowflake
from asks import Session  # type: ignore
import trio
from typing import Optional, Dict, Any, Union, Tuple, cast


class HTTPClient:
    __slots__ = ('session', 'ratelimits')
    session: Session
    ratelimits: Dict[str, Ratelimit]

    def __init__(self, token: str, session: Optional[Session] = None):
        self.session = session or Session(
            headers={
                'Authorization': f'Bot {token}',
                'User-Agent': r'yu1za1 (N/A, sun.0)'
            }
        )

        self.ratelimits = {
            '': Ratelimit(),
            'global': Ratelimit(50, 1)
        }

    async def request(
        self,
        route: Union[RouteData,
                     Tuple[HTTPMethod, str, SentDataType],
                     Tuple[HTTPMethod, str]],
        data: Optional[Dict[str, Any]] = None,
        exponential_backoff_counter: int = 0,
        **kwargs: Union[int, Snowflake]
    ) -> Any:
        route = cast(RouteData, route)  # mypy + dynamic metaclasses don't mix

        # make sure that global ratelimiting is done
        await self.ratelimits.get('global', Ratelimit(50, 1)).acquire()

        url = route.route.format(**kwargs)

        # NOTE: this ratelimits a few times if you request
        #  more than the ratelimit allows all on the same
        #  major param, but this relatively minor thing that
        #  is automatically corrected is not worth making
        #  the unlimited bucket synchronous / allow only one
        #  request at a time.
        major_params = tuple(
            v.id if isinstance(v, Snowflake) else v
            for k, v in kwargs.items() if k in
            [
                'channel_id',
                'guild_id',
                'webhook_id'
            ]
        )
        bucket = self.ratelimits.get(route.hash, Ratelimit())
        await bucket.acquire(major_params)

        # asks requires differently named kwargs
        # for different types of data: this isn't
        # a problem worth going to the low-level
        # where basically all the kwargs would be
        # unified.
        asks_kwargs = {}

        if route.datatype == SentDataType.JSON and data:
            asks_kwargs['json'] = data
        elif route.datatype == SentDataType.FILE and data:
            asks_kwargs['files'] = data
        elif route.datatype == SentDataType.QUERY and data:
            if route.method == HTTPMethod.GET:
                asks_kwargs['query'] = data
            else:
                asks_kwargs['data'] = data

        if not data:
            asks_kwargs = {}

        resp = await self.session.request(
            route.method.value,
            url,
            **asks_kwargs
        )

        # if we are globally ratelimited,
        # reschedule the request, and
        # make sure the locally stored
        # global ratelimit is representative
        # of what is on discord's end
        if resp.headers.get('X-RateLimit-Global'):
            if not self.ratelimits.get('global'):
                # this might have been the problem
                self.ratelimits['global'] = Ratelimit(50, 1, (), 50)
            else:
                self.ratelimits['global'].containers[()].uses = 50

            await trio.sleep(2 ** exponential_backoff_counter)
            return await self.request(
                route,
                data,
                exponential_backoff_counter + 1,
                **kwargs
            )

        # if we were ratelimited (not globally though
        # as that was sifted out above), then just
        # check for a Discord outage or Cloudflare
        # ban or something, and reschedule
        if resp.status_code == 429:
            if not resp.headers.get('Via'):
                raise ExternalException(
                    # external error haiku
                    'Something weird happened:\n'
                    'Cloudflare, Discord, your proxy...\n'
                    'One of them is wack.'
                )

            # ratelimited! try again, hopefully
            # something better will happen...

            # make sure that the api doesn't get DoSed
            await trio.sleep(2 ** (exponential_backoff_counter - 3))
            return await self.request(
                route,
                data,
                exponential_backoff_counter + 1,
                **kwargs
            )

        # this gets run every time, but I have no idead
        # whether one of these signals the rest is present
        ratelimit_headers_present = (
            resp.headers.get('X-RateLimit-Bucket')
            and resp.headers.get('X-RateLimit-Limit')
            and resp.headers.get('X-RateLimit-Reset-After')
            and resp.headers.get('X-RateLimit-Remaining')
        )

        # if this is the first request with ratelimit
        # headers present, update which bucket this Route
        # points to and update said bucket too.
        if route.hash == '' and ratelimit_headers_present:
            route.hash = resp.headers['X-Ratelimit-Bucket']
            previous_requests = (int(resp.headers['X-RateLimit-Limit'])
                                 - int(resp.headers['X-RateLimit-Remaining']))

            if not self.ratelimits.get(route.hash):
                bucket = Ratelimit(
                    int(resp.headers['X-RateLimit-Limit']),
                    int(resp.headers['X-RateLimit-Reset-After']),
                    tuple(major_params),
                    previous_requests
                )
                self.ratelimits[route.hash] = bucket

            if previous_requests > 1:
                # uh oh someone's been here, our refresh time is off
                route.resets_in_complete = False
            else:
                route.resets_in_complete = True

        if not route.resets_in_complete and ratelimit_headers_present:
            previous_requests = (int(resp.headers['X-RateLimit-Limit'])
                                 - int(resp.headers['X-RateLimit-Remaining']))

            if previous_requests == 1:
                route.resets_in_complete = True
                new_refresh = resp.headers['X-RateLimit-Reset-After']
                self.ratelimits[route.hash].refresh = new_refresh

        return resp
