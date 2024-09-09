import sqlalchemy as sa
import sqlalchemy.orm as orm

from datetime import datetime
from kringlecraft.data.modelbase import SqlAlchemyBase


class Invitation(SqlAlchemyBase):
    """Represents an invitation. An invitation can be distributed to share a solution.
    """
    __tablename__ = 'invitations'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'))
    world_id: int = sa.Column(sa.Integer, sa.ForeignKey('worlds.id', ondelete='CASCADE'))
    # objective_id: int = sa.Column(sa.Integer, sa.ForeignKey('objectives.id', ondelete='CASCADE'))
    code: str = sa.Column(sa.String, nullable=False)
    usage: str = sa.Column(sa.String, nullable=True)
    counter: int = sa.Column(sa.Integer, nullable=False, default=0)
    created_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    modified_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    user = orm.relationship('User', backref='invitation_to_users', passive_deletes=True)
    world = orm.relationship('World', backref='invitation_to_worlds', passive_deletes=True)
    # objective = orm.relationship('Objective', backref='invitation_to_objectives', passive_deletes=True)

    def __repr__(self):
        return '<Invitation {}>'.format(self.id)
