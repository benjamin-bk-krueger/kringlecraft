import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from kringlecraft.data.modelbase import SqlAlchemyBase

__factory = None  # implement factory pattern this way


def global_init(db_file: str, echo: bool = False):
    """Initializes the database using the factory pattern.
    :param str db_file: Path to the database file.
    :param bool echo: Print SQL statements to the console.
    """
    global __factory

    if __factory:
        pass

    if not db_file or not db_file.strip():
        raise FileNotFoundError('You must specify a db file.')

    conn_str = 'sqlite:///' + db_file.strip()
    print('INFO: Connecting to DB with {}'.format(conn_str))

    # Set check_same_thread = False. This can be an issue about creating / owner thread when cleaning up sessions, etc.
    # This is a sqlite restriction that we don't care about here.
    engine = sa.create_engine(conn_str, echo=echo, connect_args={'check_same_thread': False})
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import kringlecraft.data.__all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """Create a new DB session using the factory pattern.
    :return: A new DB session.
    """
    global __factory

    session: Session = __factory()  # NOQA

    session.expire_on_commit = False

    return session
