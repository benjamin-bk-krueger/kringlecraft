import kringlecraft.data.db_session as db_session
from kringlecraft.data.worlds import World
from kringlecraft.utils.file_tools import (file_hash, check_path, web_path, dummy_path, get_temp_file, file_ending,
                                           rename_temp_file)


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


def find_world_by_id(world_id: int) -> World | None:
    session = db_session.create_session()
    try:
        return session.query(World).filter(World.id == world_id).first()
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


def get_world_image(world_id: int) -> str | None:
    session = db_session.create_session()
    try:
        world = session.query(World).filter(World.id == world_id).first()

        if world.image is not None and check_path("world", world.image):
            return web_path("world", world.image)
        else:
            return dummy_path()
    finally:
        session.close()


# ----------- Edit functions -----------
def edit_world(world_id: int, name: str = None, description: str = None, url: str = None, visible: bool = None, archived: bool = None) -> World | None:
    session = db_session.create_session()
    try:
        world = session.query(World).filter(World.id == world_id).first()
        if world:
            world.name = name if name is not None else world.name
            world.description = description if description is not None else world.description
            world.url = url if url is not None else world.url
            world.visible = visible if visible is not None else world.visible
            world.archived = archived if archived is not None else world.archived

            session.commit()

            print(f"INFO: World information changed for world {world.name}")

            return world
    finally:
        session.close()


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
            temp_file = get_temp_file("world")
            if temp_file:
                rename_temp_file("world", temp_file, file_hash(world.name), file_ending(temp_file))
                world.image = file_hash(world.name) + "." + file_ending(temp_file)

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
def delete_world(world_id: int) -> World | None:
    session = db_session.create_session()
    try:
        world = session.query(World).filter(World.id == world_id).first()
        if world:
            session.query(World).filter(World.id == world_id).delete()
            session.commit()

            print(f"INFO: World {world.name} deleted")

            return world
    finally:
        session.close()
