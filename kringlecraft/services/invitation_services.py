import kringlecraft.data.db_session as db_session

from kringlecraft.data.invitations import Invitation
from kringlecraft.services.__all_services import find_one, find_all
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
    if find_invitation_by_id(invitation_id):
        session = db_session.create_session()
        try:
            invitation = session.query(Invitation).filter(Invitation.id == invitation_id).first()
            if invitation:
                invitation.counter = invitation.counter + 1
                session.commit()

                print(f"INFO: Usage counter increased for invitation id:{invitation_id}")

                return invitation
        finally:
            session.close()


# ----------- Create functions -----------

def create_link_for_world(world_id: int, usage: str, user_id: int) -> Invitation | None:
    # create a new invitation link for the given world
    invitation = Invitation()
    invitation.code = random_hash()
    invitation.usage = "<Unknown>" if usage == "" else usage
    invitation.world_id = world_id
    invitation.user_id = user_id

    session = db_session.create_session()
    try:
        session.add(invitation)
        session.commit()

        print(f"INFO: A new invitation for world id {world_id} has been created")

        return invitation
    finally:
        session.close()


# ----------- Delete functions -----------
def delete_invitation_for_user(invitation_id: int, user_id: int) -> Invitation | None:
    session = db_session.create_session()
    try:
        invitation = session.query(Invitation).filter(Invitation.id == invitation_id).filter(Invitation.user_id ==
                                                                                             user_id).first()
        if invitation:
            session.query(Invitation).filter(Invitation.id == invitation_id).filter(Invitation.user_id ==
                                                                                    user_id).delete()
            session.commit()

            print(f"INFO: Invitation id {invitation_id} deleted")

            return invitation
    finally:
        session.close()
