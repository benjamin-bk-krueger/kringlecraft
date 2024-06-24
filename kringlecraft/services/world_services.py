import os

import kringlecraft.data.db_session as db_session
from kringlecraft.data.worlds import World


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
            if world.image is not None and os.path.isfile(os.path.join('static/uploads/world/', world.image)):
                images[world.id] = os.path.join('uploads/world/', world.image)
            else:
                images[world.id] = "img/not_found.jpg"

        return images
    finally:
        session.close()


# ----------- Create functions -----------
def create_world(name: str, description: str, url: str, visible: bool, archived: bool) -> World | None:
    if find_world_by_name(name):
        return None

    world = World()
    world.name = name
    world.description = description
    world.url = url
    world.visible = visible
    world.archived = archived

    session = db_session.create_session()
    try:
        session.add(world)
        session.commit()

        print(f"INFO: A new world {world.name} has been created")

        return world
    finally:
        session.close()
