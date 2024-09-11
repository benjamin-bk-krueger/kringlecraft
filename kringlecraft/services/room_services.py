import kringlecraft.data.db_session as db_session

from kringlecraft.data.rooms import Room
from kringlecraft.services.__all_services import (get_count, find_all, find_one, delete, get_choices)


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
    session = db_session.create_session()
    try:
        room = session.query(Room).filter(Room.id == room_id).first()
        if room:
            room.name = name if name is not None else room.name
            room.description = description if description is not None else room.description
            room.world_id = world_id if world_id is not None else room.world_id

            session.commit()

            print(f"INFO: Room information changed for room {room.name}")

            return room
    finally:
        session.close()


# ----------- Create functions -----------
def create_room(name: str, description: str, world_id: int, user_id: int) -> Room | None:
    if find_world_room_by_name(world_id, name):
        return None

    room = Room()
    room.name = name
    room.description = description
    room.world_id = world_id
    room.user_id = user_id

    session = db_session.create_session()
    try:
        session.add(room)
        session.commit()

        print(f"INFO: A new room {room.name} has been created")

        return room
    finally:
        session.close()


# ----------- Delete functions -----------
def delete_room(room_id: int) -> Room | None:
    return delete(Room, id=room_id)
