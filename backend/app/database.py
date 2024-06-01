import logging

from app.config import settings
from app.exceptions.soft_delete import SoftDeleteNotSupported
from app.utils.time_utils import datetime_to_str, utcnow
from sqlalchemy import Boolean, Column, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.session import Session

log = logging.getLogger(__name__)

engine = create_engine(str(settings.SQLALCHEMY_DB_URL), echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True, default=None)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = utcnow()
        return self

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        return self

    @property
    def deleted_at_str(self):
        if self.deleted_at is None:
            return None
        return datetime_to_str(self.deleted_at)


class SoftDeleteBase(Base, SoftDeleteMixin):
    __abstract__ = True


class SoftDeletSession(Session):

    def active_query(self, *args, **kwargs):
        query = self.query(*args, **kwargs)
        try:
            query = query.filter_by(is_deleted=False)
        except Exception as ex:
            log.error(f"active query failed: {ex}")
            raise ex
        return query

    def soft_delete(self, obj):
        if not isinstance(obj, SoftDeleteBase):
            raise SoftDeleteNotSupported(obj.__class__.__name__)
        obj.soft_delete()
        self.add(obj)

    def restore(self, obj):
        if not isinstance(obj, SoftDeleteBase):
            raise SoftDeleteNotSupported(obj.__class__.__name__)
        obj.restore()
        self.add(obj)


SoftDeletSessionLocal = sessionmaker(
    class_=SoftDeletSession,
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db(soft_delete_support=True):
    """
    Returns a database session.

    :return: Database session
    :rtype: sqlalchemy.orm.Session
    """
    if soft_delete_support:
        db = SoftDeletSessionLocal()
    else:
        db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
