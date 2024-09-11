from kringlecraft.data.solutions import Solution
from kringlecraft.services.__all_services import (get_count, find_one, find_all, create, edit, delete)


# ----------- Count functions -----------
def get_active_count() -> int | None:
    return get_count(Solution, visible=True, completed=True)


# ----------- Find functions -----------
def find_active_solution_by_id(solution_id: int) -> Solution | None:
    return find_one(Solution, id=solution_id, visible=True, completed=True)


def find_objective_solution_for_user(objective_id: int, user_id: int) -> Solution | None:
    return find_one(Solution, user_id=user_id, objective_id=objective_id)


def find_active_solutions(objective_id: int) -> list[Solution] | None:
    return find_all(Solution, 'created_date', objective_id=objective_id, visible=True, completed=True)


# ----------- Edit functions -----------
def set_objective_notes_for_user(objective_id: int, user_id: int, notes: bytes) -> Solution | None:
    if solution := find_objective_solution_for_user(objective_id, user_id):
        return edit(Solution, solution.id, notes=notes)


# ----------- Create functions -----------
def create_or_edit_solution(objective_id: int, user_id: int, visible: bool = None, completed: bool = None,
                            ctf_flag: str = None) -> Solution | None:
    if solution := find_objective_solution_for_user(objective_id, user_id):
        return edit(Solution, solution.id, visible=visible, completed=completed, ctf_flag=ctf_flag)

    return create(Solution, visible=visible, completed=completed, ctf_flag=ctf_flag, objective_id=objective_id, user_id=user_id)


# ----------- Delete functions -----------
def delete_solution(objective_id: int, user_id: int) -> Solution | None:
    return delete(Solution, user_id=user_id, objective_id=objective_id)
