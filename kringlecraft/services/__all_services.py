import sqlalchemy as sa
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
        entities = session.query(model)
        for key, value in kwargs.items():
            entities = entities.filter(getattr(model, key) == value)
        return entities.count()
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
        entities = session.query(model)
        for key, value in kwargs.items():
            entities = entities.filter(getattr(model, key) == value)
        return entities.order_by(sa.asc(getattr(model, order))).all()
    finally:
        session.close()


def find_one(model: Type[S], **kwargs) -> S | None:
    """Find one object of given type in the database.
    :param model: Type of object.
    :param kwargs: Keyword arguments to filter results.
    :return: Object of given type."""
    session = db_session.create_session()
    try:
        entities = session.query(model)
        for key, value in kwargs.items():
            entities = entities.filter(getattr(model, key) == value)
        return entities.first()
    finally:
        session.close()


def get_choices(entities: list[S], field_id: str = 'id', field_name: str = 'name') -> list[tuple[int, str]]:
    """Get HTML compatible choices for given models.
    :param entities: List of entities.
    :param field_id: Field name containing ID.
    :param field_name: Field name containing Name.
    :return: List of choices.
    """
    return [(getattr(entity, field_id), getattr(entity, field_name)) for entity in entities]


# ----------- Edit functions -----------
def edit(model: Type[S], entity_id=int, **kwargs) -> S | None:
    """Edit one object of given type in the database.
    :param model: Type of object.
    :param entity_id: ID of object to edit.
    :param kwargs: Keyword arguments to edit object fields.
    :return: Object of given type.
    """
    session = db_session.create_session()
    try:
        entity = session.query(model).filter(getattr(model, 'id') == entity_id).first()
        if entity:
            for key, value in kwargs.items():
                setattr(entity, key, value)

            session.commit()
            print(f"INFO: Existing {model.__name__} information changed for ID {entity_id} with values {kwargs}")

            return entity
    finally:
        session.close()


# ----------- Create functions -----------
def create(model: Type[S], **kwargs) -> S | None:
    """Create one object of given type in the database.
    :param model: Type of object.
    :param kwargs: Keyword arguments to create object fields.
    :return: Object of given type.
    """
    entity = model()
    for key, value in kwargs.items():
        setattr(entity, key, value)

    session = db_session.create_session()
    try:
        session.add(entity)
        session.commit()

        print(f"INFO: A new {model.__name__} has been created with values {kwargs}")

        return entity
    finally:
        session.close()


# ----------- Delete functions -----------
def delete(model: Type[S], **kwargs) -> S | None:
    """Delete all objects of given type in the database.
    :param model: Type of object.
    :param kwargs: Keyword arguments to filter results.
    :return: Objects of given type.
    """
    session = db_session.create_session()
    try:
        entities = session.query(model)
        for key, value in kwargs.items():
            entities = entities.filter(getattr(model, key) == value)

        entity = entities.first()
        session.delete(entity)
        session.commit()
        print(f"INFO: {model.__name__} {kwargs} deleted")

        return entity
    finally:
        session.close()
