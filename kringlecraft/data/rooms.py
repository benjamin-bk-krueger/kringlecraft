import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm

from kringlecraft.data.modelbase import SqlAlchemyBase


class Room(SqlAlchemyBase):
    """Represents a room. A room can contain several objectives.
    """
    __tablename__ = 'rooms'
    __table_args__ = (
        sa.UniqueConstraint('name', 'world_id', name='uix_room_name_world_id'),
    )

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL'))
    world_id: int = sa.Column(sa.Integer, sa.ForeignKey('worlds.id', ondelete='CASCADE'))
    name: str = sa.Column(sa.String, index=True, nullable=False)
    description: str = sa.Column(sa.String, nullable=True)
    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    modified_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    user = orm.relationship('User', backref='rooms_to_users', passive_deletes=True)
    world = orm.relationship('World', backref='rooms_to_worlds', passive_deletes=True)

    def __repr__(self):
        return '<Room {}>'.format(self.name)
