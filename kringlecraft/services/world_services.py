import kringlecraft.data.db_session as db_session
from kringlecraft.data.worlds import World
from kringlecraft.services.__all_services import (get_count, find_all, find_by_id, find_by_field, delete,
                                                  get_choices)


# ----------- Count functions -----------
def get_world_count() -> int | None:
    return get_count(World)


# ----------- Find functions -----------
def find_all_worlds() -> list[World] | None:
    return find_all(World)


def find_world_by_id(world_id: int) -> World | None:
    return find_by_id(World, world_id)


def find_world_by_name(name: str) -> World | None:
    return find_by_field(World, 'name', name)


def get_world_choices(worlds: list[World]) -> list[tuple[int, str]]:
    return get_choices(worlds)


# ----------- Edit functions -----------
def edit_world(world_id: int, name: str = None, description: str = None, url: str = None, visible: bool = None,
               archived: bool = None) -> World | None:
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
    return delete(World, world_id)
