from sqlalchemy import asc
from typing import TypeVar, Type
import kringlecraft.data.db_session as db_session


T = TypeVar('T')


# ----------- Count functions -----------
def get_count(model: Type[T]) -> int | None:
    session = db_session.create_session()
    try:
        return session.query(model).count()
    finally:
        session.close()


# ----------- Find functions -----------
def find_all(model: Type[T], order_by_field: str = 'name') -> list[T] | None:
    session = db_session.create_session()
    try:
        return session.query(model).order_by(asc(getattr(model, order_by_field))).all()
    finally:
        session.close()


def find_by_id(model: Type[T], entity_id: int) -> T | None:
    session = db_session.create_session()
    try:
        return session.query(model).filter(model.id == entity_id).first()
    finally:
        session.close()


def find_by_field(model: Type[T], field: str, value) -> T | None:
    session = db_session.create_session()
    try:
        return session.query(model).filter(getattr(model, field) == value).first()
    finally:
        session.close()


def get_choices(entities: list[T], id_field: str = 'id', name_field: str = 'name') -> list[tuple[int, str]]:
    return [(getattr(entity, id_field), getattr(entity, name_field)) for entity in entities]


# ----------- Delete functions -----------
def delete(model: Type[T], entity_id: int, id_field: str = 'id', name_field: str = 'name') -> T | None:
    session = db_session.create_session()
    try:
        entity = session.query(model).filter(getattr(model, id_field) == entity_id).first()
        if entity:
            session.query(model).filter(getattr(model, id_field) == entity_id).delete()
            session.commit()

            entity_name = getattr(entity, name_field)
            print(f"INFO: {model.__name__} {entity_name} deleted")

            return entity
    finally:
        session.close()
