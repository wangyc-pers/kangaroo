from app.core.snowflake import snowflake
from app.database import SoftDeleteBase as DeclarativeBase
from app.utils.base58_utils import int_to_str
from app.utils.time_utils import datetime_to_str, utcnow
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)


class BaseModel(TimestampMixin, DeclarativeBase):
    __abstract__ = True
    ID_PREFIX = "id"

    id = Column(
        Integer, primary_key=True,
        index=True, default=snowflake.get_id
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

    @property
    def id_str(self):
        return int_to_str(self.id, prefix=self.ID_PREFIX)

    @property
    def created_at_str(self):
        return datetime_to_str(self.created_at)

    @property
    def updated_at_str(self):
        return datetime_to_str(self.updated_at)

    @property
    def deleted_at_str(self):
        if self.deleted_at is None:
            return None
        return datetime_to_str(self.deleted_at)

    def to_dict(self, include=None, exclude=None):
        """Return a dict representation of the model."""
        data = {}
        if exclude is None:
            exclude = []
        exclude.extend(["is_deleted", "deleted_at", "deleted_at_str"])
        cls_keys = list(self.__mapper__.c.keys())
        property_keys = [attr for attr in dir(self) if hasattr(type(self), attr) and isinstance(getattr(type(self), attr), property)]
        keys = set(cls_keys).union(property_keys)
        if include:
            include = set(include)
            keys = keys.intersection(include)
        if exclude:
            exclude = set(exclude)
            keys = keys.difference(exclude)
        for key in keys:
            data[key] = getattr(self, key)
        return data
