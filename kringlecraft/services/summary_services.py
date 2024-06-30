import kringlecraft.data.db_session as db_session
from kringlecraft.data.summaries import Summary


# ----------- Find functions -----------
def find_world_summary_for_user(world_id: int, user_id: int) -> Summary | None:
    session = db_session.create_session()
    try:
        return session.query(Summary).filter(Summary.user_id == user_id).filter(Summary.world_id == world_id).first()
    finally:
        session.close()


# ----------- Edit functions -----------
def set_world_notes_for_user(world_id: int, user_id: int, notes: bytes) -> Summary | None:
    session = db_session.create_session()
    try:
        summary = session.query(Summary).filter(Summary.user_id == user_id).filter(Summary.world_id == world_id).first()
        if summary:
            summary.notes = notes
            session.commit()

            print(f"INFO: Summary notes changed for world id:{world_id}")

            return summary
    finally:
        session.close()


# ----------- Create functions -----------
def create_or_edit_summary(world_id: int, user_id: int, visible: bool = None) -> Summary | None:
    if find_world_summary_for_user(world_id, user_id):
        session = db_session.create_session()
        try:
            summary = session.query(Summary).filter(Summary.user_id == user_id).filter(
                Summary.world_id == world_id).first()
            if summary:
                summary.visible = visible if visible is not None else summary.visible
                session.commit()

                print(f"INFO: Summary notes changed for world id:{world_id}")

                return summary
        finally:
            session.close()

    summary = Summary()
    summary.visible = visible
    summary.world_id = world_id
    summary.user_id = user_id

    session = db_session.create_session()
    try:
        session.add(summary)
        session.commit()

        print(f"INFO: A new summary {summary.id} has been created")

        return summary
    finally:
        session.close()
