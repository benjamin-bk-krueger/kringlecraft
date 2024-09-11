import kringlecraft.data.db_session as db_session

from kringlecraft.data.users import User
from kringlecraft.services.__all_services import (get_count, find_all, find_one, delete, get_choices)
from kringlecraft.utils.misc_tools import (random_hash, hash_text, verify_hash)
from kringlecraft.utils.constants import Role  # Import the constants


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
    return find_all(User, 'name')


def find_user_by_id(user_id: int) -> User | None:
    return find_one(User, id=user_id)


def find_user_by_email(email: str) -> User | None:
    return find_one(User, email=email)


def get_user_choices(users: list[User]) -> list[tuple[int, str]]:
    return get_choices(users)


def find_active_users() -> list[User] | None:
    return find_all(User, 'name', active=True)


def find_active_user_by_id(user_id: int) -> User | None:
    return find_one(User, active=True, id=user_id)


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
    # check a valid student account and enable an account
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
    # check a valid student account and sent out password reset mail
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


# ----------- Create functions -----------
def create_user(name: str, email: str, password: str) -> User | None:
    if find_user_by_email(email):
        return None

    user = User()
    user.email = email
    user.name = name
    user.hashed_password = hash_text(password)
    user.role = Role.USER.value
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


# ----------- Delete functions -----------
def delete_user(user_id: int) -> User | None:
    return delete(User, id=user_id)
