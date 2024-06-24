import os
import glob

import kringlecraft.data.db_session as db_session
from kringlecraft.data.worlds import World
from kringlecraft.services.misc_services import (check_path, web_path, dummy_path, file_hash)


# ----------- Count functions -----------
def get_world_count() -> int | None:
    session = db_session.create_session()
    try:
        return session.query(World).count()
    finally:
        session.close()


# ----------- Find functions -----------
def find_all_worlds() -> list[World] | None:
    session = db_session.create_session()
    try:
        return session.query(World).order_by(World.name.asc()).all()
    finally:
        session.close()


def find_world_by_name(name: str) -> World | None:
    session = db_session.create_session()
    try:
        return session.query(World).filter(World.name == name).first()
    finally:
        session.close()


def get_all_images() -> dict | None:
    session = db_session.create_session()
    try:
        images = dict()
        worlds = session.query(World).order_by(World.name.asc()).all()

        for world in worlds:
            if world.image is not None and check_path("world", world.image):
                images[world.id] = web_path("world", world.image)
            else:
                images[world.id] = dummy_path()

        return images
    finally:
        session.close()


def get_temp_image() -> str | None:
    temp_files = glob.glob(os.path.join('static/uploads/world/', "_temp.*"))
    if temp_files:
        # Return the first match; you can modify this to return all matches if needed
        return temp_files[0]


# ----------- Edit functions -----------
def set_world_image(world_id: int, image: str) -> World | None:
    session = db_session.create_session()
    try:
        world = session.query(World).filter(World.id == world_id).first()
        if world:
            world.image = image

            session.commit()

            print(f"INFO: Image changed for world {world.email}")

            return world
    finally:
        session.close()


def enable_world_image(world_id: int) -> World | None:
    session = db_session.create_session()
    try:
        world = session.query(World).filter(World.id == world_id).first()
        if world:
            temp_file = get_temp_image()
            if temp_file:
                my_hash = file_hash(world.name)
                ending = os.path.splitext(temp_file)[1][1:]
                os.rename(temp_file, os.path.join('static/uploads/world/', my_hash + "." + ending))

                world.image = my_hash + "." + ending

                session.commit()

                print(f"INFO: Image changed for world {world.name}")

                return world
    finally:
        session.close()


# ----------- Create functions -----------
def create_world(name: str, description: str, url: str, visible: bool, archived: bool, user_id: int) -> World | None:
    if find_world_by_name(name):
        return None

    world = World()
    world.name = name
    world.description = description
    world.url = url
    world.visible = visible
    world.archived = archived
    world.user_id = user_id

    session = db_session.create_session()
    try:
        session.add(world)
        session.commit()

        print(f"INFO: A new world {world.name} has been created")

        return world
    finally:
        session.close()


# ----------- Delete functions -----------
def delete_temp_files():
    temp_files = glob.glob(os.path.join('static/uploads/world/', "_temp.*"))
    for file_path in temp_files:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"FILE: Error deleting {file_path}: {e}")
