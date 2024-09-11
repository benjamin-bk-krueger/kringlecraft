from kringlecraft.data.users import User
from kringlecraft.services.__all_services import (get_count, find_one, find_all, create, edit, delete, get_choices)
from kringlecraft.utils.misc_tools import (random_hash, hash_text, verify_hash)
from kringlecraft.utils.constants import Role  # Import the constants


# ----------- Login functions -----------
def login_user(email: str, password: str) -> User | None:
    print(f"INFO: Try to LOGIN user {email} - ", end="")
    if user := find_one(User, email=email):
        if verify_hash(user.hashed_password, password):
            print("SUCCESS")
            return user
        else:
            print("FAILED")
            return None
    else:
        print("NOT FOUND")
        return None


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
    return edit(User, user_id, email=email, description=description, notification=notification)


def change_user_password(user_id: int, password: str) -> User | None:
    return edit(User, user_id, hashed_password=hash_text(password))


def enable_user(user_id: int) -> User | None:
    # check a valid student account and enable an account
    return edit(User, user_id, active=1)


def prepare_user(email: str) -> User | None:
    # check a valid student account and sent out password reset mail
    if user := find_one(User, active=1, email=email):
        return edit(User, user.id, reset_password=random_hash())


def reset_user(hash_value: str, password: str) -> User | None:
    # check valid student account and valid password reset link
    if user := find_one(User, active=1, reset_password=hash_value):
        return edit(User, user.id, hashed_password=hash_text(password), reset_password="")


# ----------- Create functions -----------
def create_user(name: str, email: str, password: str) -> User | None:
    if find_user_by_email(email):
        return None

    return create(User, email=email, name=name, hashed_password=hash_text(password), role=Role.USER.value, active=0, notification=0)


# ----------- Delete functions -----------
def delete_user(user_id: int) -> User | None:
    return delete(User, id=user_id)
