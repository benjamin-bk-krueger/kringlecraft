from kringlecraft.data.rooms import Room
from kringlecraft.services.__all_services import (get_count, find_one, find_all, create, edit, delete, get_choices)


# ----------- Count functions -----------
def get_room_count() -> int | None:
    return get_count(Room)


# ----------- Find functions -----------
def find_all_rooms() -> list[Room] | None:
    return find_all(Room, 'name')


def find_room_by_id(room_id: int) -> Room | None:
    return find_one(Room, id=room_id)


def find_room_by_name(name: str) -> Room | None:
    return find_one(Room, name=name)


def get_room_choices(rooms: list[Room]) -> list[tuple[int, str]]:
    return get_choices(rooms)


def find_world_rooms(world_id: int) -> list[Room] | None:
    return find_all(Room, 'name', world_id=world_id)


def find_world_room_by_name(world_id: int, name: str) -> Room | None:
    return find_one(Room, world_id=world_id, name=name)


# ----------- Edit functions -----------
def edit_room(room_id: int, world_id: int, name: str = None, description: str = None) -> Room | None:
    return edit(Room, room_id, world_id=world_id, name=name, description=description)


# ----------- Create functions -----------
def create_room(name: str, description: str, world_id: int, user_id: int) -> Room | None:
    if find_world_room_by_name(world_id, name):
        return None

    return create(Room, name=name, description=description, world_id=world_id, user_id=user_id)


# ----------- Delete functions -----------
def delete_room(room_id: int) -> Room | None:
    return delete(Room, id=room_id)
