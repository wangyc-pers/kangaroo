from app.common.security import check_password, hash_password
from app.models.base import BaseModel
from sqlalchemy import Boolean, Column, String


class User(BaseModel):
    ID_PREFIX = "us"

    email = Column(String, unique=True, index=True, nullable=False)
    _password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_password):
        self._password = hash_password(plain_password)

    def verify_password(self, plain_password):
        return check_password(plain_password, self.password)

    def soft_delete(self):
        self.email = f"del_{self.id_str}::{self.email}"
        super().soft_delete()

    def restore(self):
        self.email = self.email.split("::")[-1]
        super().restore()

    def __repr__(self):
        return f"<User(email={self.email})>"
