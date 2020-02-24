import abc
from typing import TypeVar, Any

T = TypeVar('T')


class CacheABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def pass_through(self, model: T) -> T:
        """
        Takes in a DataModel, and then outputs said datamodel.

        This method is the thing that allows your cache to take in
        data and update it's internal state. In fact, this is the
        only method that can do the above.

        This method is also where the cache fills the object with all
        the information it has stored.

        See `umbreon/cache/dict_cache.py` for a complete implementation.
        """

    @abc.abstractmethod
    def get(self, model_id: Any) -> Any:
        """
        Passes in the way the cache identifies, and returns
        the object which matches that.

        See `umbreon/cache/dict_cache.py` for a complete implementation.
        """
