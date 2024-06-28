import kringlecraft.data.db_session as db_session
from typing import List, Tuple
from kringlecraft.data.objectives import Objective
from kringlecraft.services.__all_services import (get_count, find_all, find_by_id, find_by_field, delete_entity,
                                                  get_entity_choices)


# ----------- Count functions -----------
def get_objective_count() -> int | None:
    return get_count(Objective)


# ----------- Find functions -----------
def find_all_objectives() -> list[Objective] | None:
    return find_all(Objective)


def find_objective_by_id(objective_id: int) -> Objective | None:
    return find_by_id(Objective, objective_id)


def find_objective_by_name(name: str) -> Objective | None:
    return find_by_field(Objective, 'name', name)


def get_objective_choices(objectives: List[Objective]) -> List[Tuple[int, str]]:
    return get_entity_choices(objectives)


def find_room_objectives(room_id: int) -> list[Objective] | None:
    session = db_session.create_session()
    try:
        return session.query(Objective).filter(Objective.room_id == room_id).order_by(Objective.name.asc()).all()
    finally:
        session.close()


def find_room_objective_by_name(room_id: int, name: str) -> Objective | None:
    session = db_session.create_session()
    try:
        return session.query(Objective).filter(Objective.room_id == room_id).filter(Objective.name == name).first()
    finally:
        session.close()


def get_objective_type_choices() -> list[tuple[int, str]]:
    objective_reverse = {1: "objective", 2: "character", 3: "item"}
    objective_type_choices = list()
    for key, value in objective_reverse.items():
        objective_type_choices.append((key, value.title()))
    return objective_type_choices


def get_objective_types() -> dict[int, str]:
    objective_reverse = {1: "objective", 2: "character", 3: "item"}
    objective_type_choices = dict()
    for key, value in objective_reverse.items():
        objective_type_choices[key] = value.title()
    return objective_type_choices


def get_objective_challenge(objective_id: int) -> str | None:
    session = db_session.create_session()
    try:
        objective = session.query(Objective).filter(Objective.id == objective_id).first()
        return "New challenge" if objective.challenge is None else str(bytes(objective.challenge), 'utf-8')
    finally:
        session.close()


# ----------- Edit functions -----------
def edit_objective(objective_id: int, room_id: int, name: str = None, description: str = None, difficulty: int = 1,
                   visible: bool = False, objective_type: int = 1) -> Objective | None:
    session = db_session.create_session()
    try:
        objective = session.query(Objective).filter(Objective.id == objective_id).first()
        if objective:
            objective.name = name if name is not None else objective.name
            objective.description = description if description is not None else objective.description
            objective.difficulty = difficulty if difficulty is not None else objective.difficulty
            objective.visible = visible if visible is not None else objective.visible
            objective.type = objective_type if objective_type is not None else objective.type
            objective.room_id = room_id if room_id is not None else objective.room_id

            session.commit()

            print(f"INFO: Objective information changed for objective {objective.name}")

            return objective
    finally:
        session.close()


def set_objective_challenge(objective_id: int, challenge: bytes) -> Objective | None:
    session = db_session.create_session()
    try:
        objective = session.query(Objective).filter(Objective.id == objective_id).first()
        if objective:
            objective.challenge = challenge
            session.commit()

            print(f"INFO: Challenge changed for {objective.name}")

            return objective
    finally:
        session.close()


# ----------- Create functions -----------
def create_objective(name: str, description: str, difficulty: int, visible: bool, objective_type: int, room_id: int,
                     user_id: int) -> Objective | None:
    if find_room_objective_by_name(room_id, name):
        return None

    objective = Objective()
    objective.name = name
    objective.description = description
    objective.difficulty = difficulty
    objective.visible = visible
    objective.type = objective_type
    objective.room_id = room_id
    objective.user_id = user_id

    session = db_session.create_session()
    try:
        session.add(objective)
        session.commit()

        print(f"INFO: A new objective {objective.name} has been created")

        return objective
    finally:
        session.close()


# ----------- Delete functions -----------
def delete_objective(objective_id: int) -> Objective | None:
    return delete_entity(Objective, objective_id)
