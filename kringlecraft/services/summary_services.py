import kringlecraft.data.db_session as db_session
from kringlecraft.data.summaries import Summary


# ----------- Find functions -----------
def find_world_summary_for_user(world_id: int, user_id: str) -> Summary | None:
    session = db_session.create_session()
    try:
        return session.query(Summary).filter(Summary.user_id == user_id).filter(Summary.world_id == world_id).first()
    finally:
        session.close()
