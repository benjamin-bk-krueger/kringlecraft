from sqlalchemy import asc
from typing import TypeVar, Type, List, Any, Dict, Tuple
import kringlecraft.data.db_session as db_session
from kringlecraft.utils.file_tools import (file_hash, check_path, web_path, dummy_path, get_temp_file, file_ending,
                                           rename_temp_file)

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


def get_all_images(model: Type[T], image_type: str) -> Dict[int, str] | None:
    session = db_session.create_session()
    try:
        images = {}
        entities = session.query(model).order_by(model.name.asc()).all()

        for entity in entities:
            if entity.image is not None and check_path(image_type, entity.image):
                images[entity.id] = web_path(image_type, entity.image)
            else:
                images[entity.id] = dummy_path()

        return images
    finally:
        session.close()


def get_entity_image(model: Type[T], entity_id: int, image_type: str) -> str | None:
    session = db_session.create_session()
    try:
        entity = session.query(model).filter(model.id == entity_id).first()

        if entity and entity.image is not None and check_path(image_type, entity.image):
            return web_path(image_type, entity.image)
        else:
            return dummy_path()
    finally:
        session.close()


def get_entity_choices(entities: List[T], id_field: str = 'id', name_field: str = 'name') -> List[Tuple[int, str]]:
    return [(getattr(entity, id_field), getattr(entity, name_field)) for entity in entities]


# ----------- Edit functions -----------
def set_entity_image(model: Type[T], entity_id: int, image: str, id_field: str = 'id', name_field: str = 'name') -> T | None:
    session = db_session.create_session()
    try:
        entity = session.query(model).filter(getattr(model, id_field) == entity_id).first()
        if entity:
            setattr(entity, 'image', image)
            session.commit()

            entity_name = getattr(entity, name_field)
            print(f"INFO: Image changed for {model.__name__.lower()} {entity_name}")

            return entity
    finally:
        session.close()


def enable_entity_image(model: Type[T], entity_id: int, entity_type: str, id_field: str = 'id', name_field: str = 'name') -> T | None:
    session = db_session.create_session()
    try:
        entity = session.query(model).filter(getattr(model, id_field) == entity_id).first()
        if entity:
            temp_file = get_temp_file(entity_type)
            if temp_file:
                entity_name = getattr(entity, name_field)
                new_filename = f"{file_hash(entity_name)}.{file_ending(temp_file)}"
                rename_temp_file(entity_type, temp_file, file_hash(entity_name), file_ending(temp_file))
                setattr(entity, 'image', new_filename)

                session.commit()

                print(f"INFO: Image changed for {model.__name__.lower()} {entity_name}")

                return entity
    finally:
        session.close()


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
