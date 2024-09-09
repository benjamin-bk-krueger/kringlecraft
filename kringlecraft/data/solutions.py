import sqlalchemy as sa
import sqlalchemy.orm as orm

from datetime import datetime
from kringlecraft.data.modelbase import SqlAlchemyBase


class Solution(SqlAlchemyBase):
    """Represents a solution. A solution belongs to a challenge of an objective.
    """
    __tablename__ = 'solutions'
    __table_args__ = (
        sa.UniqueConstraint('user_id', 'objective_id', name='uix_user_id_objective_id'),
    )

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'))
    objective_id: int = sa.Column(sa.Integer, sa.ForeignKey('objectives.id', ondelete='CASCADE'))
    notes: bytes = sa.Column(sa.LargeBinary, nullable=True)
    visible: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    completed: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    ctf_flag: str = sa.Column(sa.String, nullable=True)
    created_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    modified_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    user = orm.relationship('User', backref='solutions_to_users', passive_deletes=True)
    objective = orm.relationship('Objective', backref='solutions_to_objectives', passive_deletes=True)

    def __repr__(self):
        return '<Solution {}>'.format(self.id)
