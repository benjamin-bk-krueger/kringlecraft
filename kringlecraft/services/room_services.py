import kringlecraft.data.db_session as db_session
from kringlecraft.data.rooms import Room
from kringlecraft.utils.file_tools import (file_hash, check_path, web_path, dummy_path, get_temp_file, file_ending,
                                           rename_temp_file)


# ----------- Count functions -----------
def get_room_count() -> int | None:
    session = db_session.create_session()
    try:
        return session.query(Room).count()
    finally:
        session.close()


# ----------- Find functions -----------
def find_all_rooms() -> list[Room] | None:
    session = db_session.create_session()
    try:
        return session.query(Room).order_by(Room.name.asc()).all()
    finally:
        session.close()


def find_world_rooms(world_id: int) -> list[Room] | None:
    session = db_session.create_session()
    try:
        return session.query(Room).filter(Room.world_id == world_id).order_by(Room.name.asc()).all()
    finally:
        session.close()


def find_room_by_id(room_id: int) -> Room | None:
    session = db_session.create_session()
    try:
        return session.query(Room).filter(Room.id == room_id).first()
    finally:
        session.close()


def find_room_by_name(name: str) -> Room | None:
    session = db_session.create_session()
    try:
        return session.query(Room).filter(Room.name == name).first()
    finally:
        session.close()


def find_world_room_by_name(world_id: int, name: str) -> Room | None:
    session = db_session.create_session()
    try:
        return session.query(Room).filter(Room.world_id == world_id).filter(Room.name == name).first()
    finally:
        session.close()


def get_all_images() -> dict | None:
    session = db_session.create_session()
    try:
        images = dict()
        rooms = session.query(Room).order_by(Room.name.asc()).all()

        for room in rooms:
            if room.image is not None and check_path("room", room.image):
                images[room.id] = web_path("room", room.image)
            else:
                images[room.id] = dummy_path()

        return images
    finally:
        session.close()


def get_room_image(room_id: int) -> str | None:
    session = db_session.create_session()
    try:
        room = session.query(Room).filter(Room.id == room_id).first()

        if room.image is not None and check_path("room", room.image):
            return web_path("room", room.image)
        else:
            return dummy_path()
    finally:
        session.close()


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


def set_room_image(room_id: int, image: str) -> Room | None:
    session = db_session.create_session()
    try:
        room = session.query(Room).filter(Room.id == room_id).first()
        if room:
            room.image = image

            session.commit()

            print(f"INFO: Image changed for room {room.name}")

            return room
    finally:
        session.close()


def enable_room_image(room_id: int) -> Room | None:
    session = db_session.create_session()
    try:
        room = session.query(Room).filter(Room.id == room_id).first()
        if room:
            temp_file = get_temp_file("room")
            if temp_file:
                rename_temp_file("room", temp_file, file_hash(room.name), file_ending(temp_file))
                room.image = file_hash(room.name) + "." + file_ending(temp_file)

                session.commit()

                print(f"INFO: Image changed for room {room.name}")

                return room
    finally:
        session.close()


def get_room_choices(rooms: list[Room]) -> list[tuple[int, str]]:
    rooms_choices = list()
    for room in rooms:
        rooms_choices.append((room.id, room.name))
    return rooms_choices


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
    session = db_session.create_session()
    try:
        room = session.query(Room).filter(Room.id == room_id).first()
        if room:
            session.query(Room).filter(Room.id == room_id).delete()
            session.commit()

            print(f"INFO: Room {room.name} deleted")

            return room
    finally:
        session.close()
