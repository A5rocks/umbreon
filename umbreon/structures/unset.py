from typing import Any, Iterable


class Unset(object):
    """A dumb class with dunders replaced..."""
    def __getattr__(self, *_: Any, **__: Any) -> 'Unset':
        return self

    def __len__(self) -> int:
        return 0

    def __iter__(self) -> Iterable[None]:
        return ()

    def __bool__(self) -> bool:
        return False
