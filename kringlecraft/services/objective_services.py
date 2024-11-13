from kringlecraft.data.objectives import Objective
from kringlecraft.services.__all_services import (get_count, find_one, find_all, create, edit, delete, get_choices)


# ----------- Count functions -----------
def get_objective_count() -> int | None:
    return get_count(Objective)


# ----------- Find functions -----------
def find_all_objectives() -> list[Objective] | None:
    return find_all(Objective, 'name')


def find_objective_by_id(objective_id: int) -> Objective | None:
    return find_one(Objective, id=objective_id)


def find_objective_by_id_enabled(objective_id: int) -> Objective | None:
    return find_one(Objective, id=objective_id, disabled=False)


def find_objective_by_name(name: str) -> Objective | None:
    return find_one(Objective, name=name)


def get_objective_choices(objectives: list[Objective]) -> list[tuple[int, str]]:
    return get_choices(objectives)


def find_room_objectives(room_id: int) -> list[Objective] | None:
    return find_all(Objective, 'name', room_id=room_id)


def find_room_objectives_enabled(room_id: int) -> list[Objective] | None:
    return find_all(Objective, 'name', room_id=room_id, disabled=False)


def find_room_objective_by_name(room_id: int, name: str) -> Objective | None:
    return find_one(Objective, room_id=room_id, name=name)


def get_objective_type_choices() -> list[tuple[int, str]]:
    return [(key, value.title()) for key, value in {1: "objective", 2: "character", 3: "item"}.items()]


def get_objective_types() -> dict[int, str]:
    return {key: value.title() for key, value in {1: "objective", 2: "character", 3: "item"}.items()}


def get_objective_challenge(objective_id: int) -> str | None:
    entity = find_one(Objective, id=objective_id)
    return "New challenge" if entity.challenge is None else str(bytes(entity.challenge), 'utf-8')


# ----------- Edit functions -----------
def edit_objective(objective_id: int, room_id: int, name: str = None, description: str = None, difficulty: int = None,
                   visible: bool = None, disabled: bool = None, objective_type: int = None) -> Objective | None:
    return edit(Objective, objective_id, room_id=room_id, name=name, description=description, difficulty=difficulty,
                visible=visible, disabled=disabled, type=objective_type)


def set_objective_challenge(objective_id: int, challenge: bytes) -> Objective | None:
    return edit(Objective, objective_id, challenge=challenge)


# ----------- Create functions -----------
def create_objective(name: str, description: str, difficulty: int, visible: bool, objective_type: int, room_id: int,
                     user_id: int) -> Objective | None:
    if find_room_objective_by_name(room_id, name):
        return None

    return create(Objective, name=name, description=description, difficulty=difficulty, visible=visible,
                  type=objective_type, room_id=room_id, user_id=user_id)


# ----------- Delete functions -----------
def delete_objective(objective_id: int) -> Objective | None:
    return delete(Objective, id=objective_id)
