from app.models.base import BaseModel
from app.utils.time_utils import utcnow
from sqlalchemy import Boolean, Column, String


class User(BaseModel):
    ID_PREFIX = "us"

    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

    def soft_delete(self):
        self.email = f"deleted_{utcnow()}::{self.email}"
        super().soft_delete()

    def restore(self):
        self.email = self.email.split("::")[-1]
        super().restore()

    def __repr__(self):
        return f"<User(email={self.email})>"
