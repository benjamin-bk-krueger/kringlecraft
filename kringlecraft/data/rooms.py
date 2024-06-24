import datetime
import sqlalchemy
import sqlalchemy.orm as orm

from kringlecraft.data.modelbase import SqlAlchemyBase


class Room(SqlAlchemyBase):
    __tablename__ = 'rooms'
    __table_args__ = (
        sqlalchemy.UniqueConstraint('name', 'world_id', name='uix_room_name_world_id'),
    )

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id: int = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='SET NULL'))
    world_id: int = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('worlds.id', ondelete='CASCADE'))
    name: str = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    description: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    modified_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    user = orm.relationship('User', backref='rooms_to_users', passive_deletes=True)
    world = orm.relationship('World', backref='rooms_to_worlds', passive_deletes=True)

    def __repr__(self):
        return '<Room {}>'.format(self.name)
