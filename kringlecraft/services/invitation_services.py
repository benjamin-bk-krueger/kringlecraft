from kringlecraft.data.invitations import Invitation
from kringlecraft.services.__all_services import (find_one, find_all, create, edit, delete)
from kringlecraft.utils.misc_tools import random_hash


# ----------- Find functions -----------
def find_invitation_by_id(invitation_id: int) -> Invitation | None:
    return find_one(Invitation, id=invitation_id)


def find_invitation_for_user(invitation_id: int, user_id: int) -> Invitation | None:
    return find_one(Invitation, id=invitation_id, user_id=user_id)


def find_invitation_for_code(invitation_code: str) -> Invitation | None:
    return find_one(Invitation, code=invitation_code)


def find_all_invitations_for_user(user_id: int) -> list[Invitation] | None:
    return find_all(Invitation, 'world_id', user_id=user_id)


# ----------- Edit functions -----------
def update_counter(invitation_id: int) -> Invitation | None:
    if invitation := find_invitation_by_id(invitation_id):
        return edit(Invitation, invitation.id, counter=invitation.counter + 1)


# ----------- Create functions -----------

def create_link_for_world(world_id: int, usage: str, user_id: int) -> Invitation | None:
    return create(Invitation, code=random_hash(), usage=usage, world_id=world_id,  user_id=user_id)


# ----------- Delete functions -----------
def delete_invitation_for_user(invitation_id: int, user_id: int) -> Invitation | None:
    return delete(Invitation, id=invitation_id, user_id=user_id)
