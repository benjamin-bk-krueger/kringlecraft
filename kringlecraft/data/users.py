import datetime
import sqlalchemy

from flask_login import UserMixin  # to manage user sessions
from kringlecraft.data.modelbase import SqlAlchemyBase


class User(UserMixin, SqlAlchemyBase):
    __tablename__ = 'users'

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email: str = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    description: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password: str = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True)
    reset_password: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role: int = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
    active: bool = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    notification: bool = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    image: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    modified_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    last_login: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)
