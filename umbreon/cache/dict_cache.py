from .cache_abc import CacheABC
from ..structures.snowflake import SnowflakeDependent
from ..structures.storage_box import StorageBox
from typing import TypeVar, Any, Dict


T = TypeVar('T')


class DictCache(CacheABC):
    __slots__ = ('backing',)
    backing: Dict[int, Any]

    def __init__(self):
        self.backing = dict()

    def pass_through(self, model: T) -> T:
        model_class = model.__class__

        if not issubclass(model_class, SnowflakeDependent):
            # this is useless unless said class has a meaningful,
            # nice __hash__ which isn't just `id`. For now that's just
            # SnowflakeDependent or IDDependent, the second of which is
            # only Snowflakes which don't need to be cached.
            return model

        # check if there is another model like that stored
        is_stored = hash(model) in self.backing

        if not is_stored:
            # maybe model should be .copy() -ed?
            self.backing[hash(model)] = model
            return model

        # a simple check to see if this should continue
        # this may happen, who knows, discord is weird
        # besides, this check doesn't take much...
        stored_model = self.backing[hash(model)]

        if type(stored_model) != type(model):
            return model

        # an assumption to make this work without taking forever
        slots = getattr(model, '__slots__', tuple())

        # light optimization:
        changes = False

        for slot in slots:
            new_data = getattr(model, slot)
            if new_data:
                if getattr(stored_model, slot) != new_data:
                    setattr(stored_model, slot, new_data)
                    changes = True

        # update storage
        if hasattr(stored_model, 'storage') and not stored_model.storage:
            stored_model.storage = StorageBox(stored_model)

        if hasattr(model, 'storage') and model.storage:  # type: ignore
            stored_model.storage.update(model.storage)  # type: ignore

        if changes:
            self.backing[hash(model)] = stored_model

        model = stored_model

        return stored_model  # type: ignore

    def get(self, model_id: Any) -> Any:
        return self.backing.get(hash(model_id))
