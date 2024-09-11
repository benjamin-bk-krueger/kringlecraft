import sqlalchemy as sa
import sqlalchemy.orm as orm
import kringlecraft.data.db_session as db_session

from kringlecraft.data.modelbase import SqlAlchemyBase
from typing import TypeVar, Type


S = TypeVar('S', bound=SqlAlchemyBase) # Can be any subtype of str


# ----------- Count functions -----------
def get_count(model: Type[S], **kwargs) -> int | None:
    """Count all objects of given type in the database.
    :param model: Type of object.
    :param kwargs: Keyword arguments to filter results.
    :return: Number of all objects of given type.
    """
    session = db_session.create_session()
    try:
        results: orm.Query = session.query(model)
        for key, value in kwargs.items():
            results = results.filter(getattr(model, key) == value)
        return results.count()
    finally:
        session.close()


# ----------- Find functions -----------
def find_all(model: Type[S], order: str, **kwargs) -> list[S] | None:
    """Find all objects of given type in the database.
    :param model: Type of object.
    :param order: Field name to sort by.
    :param kwargs: Keyword arguments to filter results.
    :return: List of all objects of given type.
    """
    session = db_session.create_session()
    try:
        results: orm.Query = session.query(model)
        for key, value in kwargs.items():
            results = results.filter(getattr(model, key) == value)
        return results.order_by(sa.asc(getattr(model, order))).all()
    finally:
        session.close()


def find_one(model: Type[S], **kwargs) -> S | None:
    """Find one object of given type in the database.
    :param model: Type of object.
    :param kwargs: Keyword arguments to filter results.
    :return: Object of given type."""
    session = db_session.create_session()
    try:
        results: orm.Query = session.query(model)
        for key, value in kwargs.items():
            results = results.filter(getattr(model, key) == value)
        return results.first()
    finally:
        session.close()


def get_choices(models: list[S], field_id: str = 'id', field_name: str = 'name') -> list[tuple[int, str]]:
    """Get HTML compatible choices for given models.
    :param models: List of models.
    :param field_id: Field name containing ID.
    :param field_name: Field name containing Name.
    :return: List of choices.
    """
    return [(getattr(model, field_id), getattr(model, field_name)) for model in models]


# ----------- Delete functions -----------
def delete(model: Type[S], **kwargs) -> S | None:
    """Delete all objects of given type in the database.
    :param model: Type of object.
    :param kwargs: Keyword arguments to filter results.
    :return: Objects of given type.
    """
    session = db_session.create_session()
    try:
        results: orm.Query = session.query(model)
        for key, value in kwargs.items():
            results = results.filter(getattr(model, key) == value)

        entity = results.first()
        session.delete(entity)
        session.commit()
        print(f"INFO: {model.__name__} {kwargs} deleted")

        return entity
    finally:
        session.close()
