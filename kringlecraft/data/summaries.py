import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm

from kringlecraft.data.modelbase import SqlAlchemyBase


class Summary(SqlAlchemyBase):
    """Represents a summary. A summary can be added to the solutions of a whole world.
    """
    __tablename__ = 'summaries'
    __table_args__ = (
        sa.UniqueConstraint('user_id', 'world_id', name='uix_user_id_world_id'),
    )

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'))
    world_id: int = sa.Column(sa.Integer, sa.ForeignKey('worlds.id', ondelete='CASCADE'))
    notes: bytes = sa.Column(sa.LargeBinary, nullable=True)
    visible: bool = sa.Column(sa.Boolean, nullable=False, default=False)
    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    modified_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    user = orm.relationship('User', backref='summaries_to_users', passive_deletes=True)
    world = orm.relationship('World', backref='summaries_to_worlds', passive_deletes=True)

    def __repr__(self):
        return '<Summary {}>'.format(self.id)
