import sqlalchemy as sa
import sqlalchemy.orm as orm

from datetime import datetime
from kringlecraft.data.modelbase import SqlAlchemyBase


class World(SqlAlchemyBase):
    """Represents a world. A world can contain several rooms.
    """
    __tablename__ = 'worlds'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL'))
    name: str = sa.Column(sa.String, index=True, unique=True, nullable=False)
    description: str = sa.Column(sa.String, nullable=True)
    url: str = sa.Column(sa.String, nullable=True)
    visible: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    archived: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    created_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    modified_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    user = orm.relationship('User', backref='worlds_to_users', passive_deletes=True)

    def __repr__(self):
        return '<World {}>'.format(self.name)
