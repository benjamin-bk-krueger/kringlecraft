import datetime
import sqlalchemy
import sqlalchemy.orm as orm

from kringlecraft.data.modelbase import SqlAlchemyBase


class World(SqlAlchemyBase):
    __tablename__ = 'worlds'

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id: int = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='SET NULL'))
    name: str = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    description: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    visible: bool = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    archived: bool = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    image: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    modified_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    user = orm.relationship('User', backref='worlds_to_users', passive_deletes=True)

    def __repr__(self):
        return '<World {}>'.format(self.name)
