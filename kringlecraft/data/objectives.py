import datetime
import sqlalchemy
import sqlalchemy.orm as orm

from kringlecraft.data.modelbase import SqlAlchemyBase


class Objective(SqlAlchemyBase):
    __tablename__ = 'objectives'
    __table_args__ = (
        sqlalchemy.UniqueConstraint('name', 'room_id', name='uix_objective_name_room_id'),
    )

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id: int = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='SET NULL'))
    room_id: int = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('rooms.id', ondelete='CASCADE'))
    name: str = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    description: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type: int = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
    difficulty: int = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
    visible: bool = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    quest: bytes = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    image: str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)
    modified_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, index=True)

    user = orm.relationship('User', backref='objectives_to_users', passive_deletes=True)
    room = orm.relationship('Room', backref='objectives_to_rooms', passive_deletes=True)

    def __repr__(self):
        return '<Objective {}>'.format(self.name)
