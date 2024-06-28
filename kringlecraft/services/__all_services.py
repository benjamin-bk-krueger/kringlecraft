from sqlalchemy import asc
from typing import TypeVar, Type, List, Any, Tuple
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
def find_all(model: Type[T], order_by_field: str = 'name') -> List[T] | None:
    session = db_session.create_session()
    try:
        return session.query(model).order_by(asc(getattr(model, order_by_field))).all()
    finally:
        session.close()


def find_by_id(model: Type[T], id: int) -> T | None:
    session = db_session.create_session()
    try:
        return session.query(model).filter(model.id == id).first()
    finally:
        session.close()


def find_by_field(model: Type[T], field: str, value: Any) -> T | None:
    session = db_session.create_session()
    try:
        return session.query(model).filter(getattr(model, field) == value).first()
    finally:
        session.close()


def get_entity_choices(entities: List[T], id_field: str = 'id', name_field: str = 'name') -> List[Tuple[int, str]]:
    return [(getattr(entity, id_field), getattr(entity, name_field)) for entity in entities]


# ----------- Delete functions -----------
def delete_entity(model: Type[T], entity_id: int, id_field: str = 'id', name_field: str = 'name') -> T | None:
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
