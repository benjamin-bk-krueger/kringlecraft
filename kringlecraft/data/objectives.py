import sqlalchemy as sa
import sqlalchemy.orm as orm

from datetime import datetime
from kringlecraft.data.modelbase import SqlAlchemyBase


class Objective(SqlAlchemyBase):
    """Represents an objective. An objective contains a challenge that needs to be solved.
    """
    __tablename__ = 'objectives'
    __table_args__ = (
        sa.UniqueConstraint('name', 'room_id', name='uix_objective_name_room_id'),
    )

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL'))
    room_id: int = sa.Column(sa.Integer, sa.ForeignKey('rooms.id', ondelete='CASCADE'))
    name: str = sa.Column(sa.String, index=True, nullable=False)
    description: str = sa.Column(sa.String, nullable=True)
    type: int = sa.Column(sa.Integer, nullable=False, default=1)
    difficulty: int = sa.Column(sa.Integer, nullable=False, default=1)
    visible: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    disabled: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    challenge: bytes = sa.Column(sa.LargeBinary, nullable=True)
    created_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    modified_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    user = orm.relationship('User', backref='objectives_to_users', passive_deletes=True)
    room = orm.relationship('Room', backref='objectives_to_rooms', passive_deletes=True)

    def __repr__(self):
        return '<Objective {}>'.format(self.name)
