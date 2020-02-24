from .base import DataModelMixin


class ClientStatus(DataModelMixin):
    __slots__ = ('desktop', 'mobile', 'web')

    desktop: str
    mobile: str
    web: str
