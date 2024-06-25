import kringlecraft.data.db_session as db_session
from typing import Dict
from kringlecraft.data.users import User
from kringlecraft.services.__all_services import (get_count, find_all, find_by_id, find_by_field, get_all_images,
                                                  get_entity_image, delete_entity, set_entity_image)
from kringlecraft.utils.misc_tools import (random_hash, hash_text, verify_hash)


# ----------- Login functions -----------
def login_user(email: str, password: str) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            print(f"INFO: Login Failure for user {email}")
            return None

        if not verify_hash(user.hashed_password, password):
            print(f"INFO: Login Failure for user {email}")
            return None

        print(f"INFO: Login Successful for user {email}")
        return user
    finally:
        session.close()


# ----------- Count functions -----------
def get_user_count() -> int | None:
    return get_count(User)


# ----------- Find functions -----------
def find_all_users() -> list[User] | None:
    return find_all(User)


def find_user_by_id(user_id: int) -> User | None:
    return find_by_id(User, user_id)


def find_user_by_email(email: str) -> User | None:
    return find_by_field(User, 'email', email)


def get_all_user_images() -> Dict[int, str] | None:
    return get_all_images(User, "profile")


def get_user_image(user_id: int) -> str | None:
    return get_entity_image(User, user_id, "profile")


def find_active_users() -> list[User] | None:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.active == True).order_by(User.name.asc()).all()
    finally:
        session.close()


def find_active_user_by_id(user_id: int) -> User | None:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.active == True).filter(User.id == user_id).first()
    finally:
        session.close()


# ----------- Create functions -----------
def create_user(name: str, email: str, password: str) -> User | None:
    if find_user_by_email(email):
        return None

    user = User()
    user.email = email
    user.name = name
    user.hashed_password = hash_text(password)
    user.role = 1
    user.active = 0
    user.notification = 0

    session = db_session.create_session()
    try:
        session.add(user)
        session.commit()

        print(f"INFO: Register approval for user {user.email}")

        return user
    finally:
        session.close()


# ----------- Edit functions -----------
def edit_user(user_id: int, email: str = None, description: str = None, notification: bool = None) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.email = email if email is not None else user.email
            user.description = description if description is not None else user.description
            user.notification = notification if notification is not None else user.notification

            session.commit()

            print(f"INFO: User information changed for user {user.email}")

            return user
    finally:
        session.close()


def set_user_image(user_id: int, image: str) -> User | None:
    return set_entity_image(User, user_id, image, name_field='email')


def change_user_password(user_id: int, password: str) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.hashed_password = hash_text(password)

            session.commit()

            print(f"INFO: User password changed for user {user.email}")

            return user
    finally:
        session.close()


def enable_user(user_id: int) -> User | None:
    # check valid student account and enable account
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.active == 0).filter(User.id == user_id).first()
        if user:
            user.active = 1
            session.commit()

            print(f"INFO: Account enabled for user {user.email}")

            return user
    finally:
        session.close()


def prepare_user(email: str) -> User | None:
    # check valid student account and sent out password reset mail
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.active == 1).filter(User.email == email).first()
        if user:
            user.reset_password = random_hash()
            session.commit()

            print(f"INFO: Reset password prepared for user {user.email}")

            return user
    finally:
        session.close()


def reset_user(hash_value: str, password: str) -> User | None:
    # check valid student account and valid password reset link
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.active == 1).filter(User.reset_password == hash_value).first()
        if user:
            user.hashed_password = hash_text(password)
            user.reset_password = ""
            session.commit()

            print(f"INFO: Password reset performed for user {user.email}")

            return user
    finally:
        session.close()


# ----------- Delete functions -----------
def delete_user(user_id: int) -> User | None:
    return delete_entity(User, user_id, name_field='email')
