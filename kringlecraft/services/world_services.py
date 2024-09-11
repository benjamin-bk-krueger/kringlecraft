from kringlecraft.data.worlds import World
from kringlecraft.services.__all_services import (get_count, find_one, find_all, create, edit, delete, get_choices)


# ----------- Count functions -----------
def get_world_count() -> int | None:
    return get_count(World)


# ----------- Find functions -----------
def find_all_worlds() -> list[World] | None:
    return find_all(World, 'name')


def find_world_by_id(world_id: int) -> World | None:
    return find_one(World, id=world_id)


def find_world_by_name(name: str) -> World | None:
    return find_one(World, name=name)


def get_world_choices(worlds: list[World]) -> list[tuple[int, str]]:
    return get_choices(worlds)


def find_active_worlds() -> list[World] | None:
    return find_all(World, 'name', archived=False)


def find_visible_worlds() -> list[World] | None:
    return find_all(World, 'name', visible=True)


# ----------- Edit functions -----------
def edit_world(world_id: int, name: str = None, description: str = None, url: str = None, visible: bool = None,
               archived: bool = None) -> World | None:
    return edit(World, world_id, name=name, description=description, url=url, visible=visible, archived=archived)


# ----------- Create functions -----------
def create_world(name: str, description: str, url: str, visible: bool, archived: bool, user_id: int) -> World | None:
    if find_world_by_name(name):
        return None

    return create(World, name, description=description, url=url, visible=visible, archived=archived, user_id=user_id)


# ----------- Delete functions -----------
def delete_world(world_id: int) -> World | None:
    return delete(World, id=world_id)
