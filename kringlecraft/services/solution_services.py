import kringlecraft.data.db_session as db_session
from kringlecraft.data.solutions import Solution


# ----------- Find functions -----------
def find_objective_solution_for_user(objective_id: int, user_id: int) -> Solution | None:
    session = db_session.create_session()
    try:
        return session.query(Solution).filter(Solution.user_id == user_id).filter(Solution.objective_id ==
                                                                                  objective_id).first()
    finally:
        session.close()


def find_active_solutions(objective_id: int) -> list[Solution] | None:
    session = db_session.create_session()
    try:
        return session.query(Solution).filter(Solution.objective_id == objective_id).filter(Solution.visible == True).filter(Solution.completed == True).order_by(Solution.created_date.asc()).all()
    finally:
        session.close()


def get_objective_notes_for_user(objective_id: int, user_id: int) -> str | None:
    session = db_session.create_session()
    try:
        solution = session.query(Solution).filter(Solution.user_id == user_id).filter(Solution.objective_id ==
                                                                                      objective_id).first()
        return "New solution" if solution is None else str(bytes(solution.notes), 'utf-8')
    finally:
        session.close()


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
def create_or_edit_solution(objective_id: int, user_id: int, visible: bool, completed: bool,
                            ctf_flag: str) -> Solution | None:
    if find_objective_solution_for_user(objective_id, user_id):
        session = db_session.create_session()
        try:
            solution = session.query(Solution).filter(Solution.user_id == user_id).filter(
                Solution.objective_id == objective_id).first()
            if solution:
                solution.visible = visible
                solution.completed = completed
                solution.ctf_flag = ctf_flag
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
