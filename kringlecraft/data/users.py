import sqlalchemy as sa

from datetime import datetime
from flask_login import UserMixin  # to manage user sessions
from kringlecraft.data.modelbase import SqlAlchemyBase


class User(UserMixin, SqlAlchemyBase):
    """Represents a user. A user is identified by their email.
    """
    __tablename__ = 'users'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name: str = sa.Column(sa.String, nullable=False)
    email: str = sa.Column(sa.String, index=True, unique=True, nullable=False)
    description: str = sa.Column(sa.String, nullable=True)
    hashed_password: str = sa.Column(sa.String, nullable=False, index=True)
    reset_password: str = sa.Column(sa.String, nullable=True)
    role: int = sa.Column(sa.Integer, nullable=False, default=1)
    active: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    notification: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    created_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    modified_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    last_login: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)
