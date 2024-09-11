from kringlecraft.data.summaries import Summary
from kringlecraft.services.__all_services import (find_one, create, edit)


# ----------- Find functions -----------
def find_world_summary_for_user(world_id: int, user_id: int) -> Summary | None:
    return find_one(Summary, user_id=user_id, world_id=world_id)


# ----------- Edit functions -----------
def set_world_notes_for_user(world_id: int, user_id: int, notes: bytes) -> Summary | None:
    if summary := find_world_summary_for_user(world_id, user_id):
        return edit(Summary, summary.id, notes=notes)


# ----------- Create functions -----------
def create_or_edit_summary(world_id: int, user_id: int, visible: bool = None) -> Summary | None:
    if summary := find_world_summary_for_user(world_id, user_id):
        return edit(Summary, summary.id, visible=visible)

    return create(Summary, visible=visible, world_id=world_id, user_id=user_id)
