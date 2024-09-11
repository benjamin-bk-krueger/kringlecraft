import kringlecraft.data.db_session as db_session

from kringlecraft.data.solutions import Solution
from kringlecraft.services.__all_services import (get_count, find_one, find_all)


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
    session = db_session.create_session()
    try:
        solution = session.query(Solution).filter(Solution.user_id == user_id).filter(Solution.objective_id ==
                                                                                      objective_id).first()
        if solution:
            solution.notes = notes
            session.commit()

            print(f"INFO: Solution notes changed for objective id:{objective_id}")

            return solution
    finally:
        session.close()


# ----------- Create functions -----------
def create_or_edit_solution(objective_id: int, user_id: int, visible: bool = None, completed: bool = None,
                            ctf_flag: str = None) -> Solution | None:
    if find_objective_solution_for_user(objective_id, user_id):
        session = db_session.create_session()
        try:
            solution = session.query(Solution).filter(Solution.user_id == user_id).filter(
                Solution.objective_id == objective_id).first()
            if solution:
                solution.visible = visible if visible is not None else solution.visible
                solution.completed = completed if completed is not None else solution.completed
                solution.ctf_flag = ctf_flag if ctf_flag is not None else solution.ctf_flag
                session.commit()

                print(f"INFO: Solution notes changed for objective id:{objective_id}")

                return solution
        finally:
            session.close()

    solution = Solution()
    solution.visible = visible
    solution.completed = completed
    solution.ctf_flag = ctf_flag
    solution.objective_id = objective_id
    solution.user_id = user_id

    session = db_session.create_session()
    try:
        session.add(solution)
        session.commit()

        print(f"INFO: A new solution {solution.id} has been created")

        return solution
    finally:
        session.close()


# ----------- Delete functions -----------
def delete(objective_id: int, user_id: int) -> Solution | None:
    session = db_session.create_session()
    try:
        solution = session.query(Solution).filter(Solution.user_id == user_id).filter(Solution.objective_id ==
                                                                                      objective_id).first()
        if solution:
            session.query(Solution).filter(Solution.user_id == user_id).filter(Solution.objective_id ==
                                                                               objective_id).delete()
            session.commit()

            print(f"INFO: Solution {Solution.__name__} deleted")

            return solution
    finally:
        session.close()
