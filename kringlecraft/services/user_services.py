import os
import random
import string
import hashlib

from passlib.handlers.sha2_crypt import sha512_crypt as crypto
import kringlecraft.data.db_session as db_session
from kringlecraft.data.users import User


def random_hash() -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


def hash_text(text: str) -> str:
    return crypto.encrypt(text, rounds=171204)


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def user_hash(user_email: str) -> str:
    return hashlib.md5(user_email.encode('utf-8')).hexdigest()


def login_user(user_email: str, user_password: str) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.email == user_email).first()
        if not user:
            print(f"INFO: Login Failure for user {user_email}")
            return None

        if not verify_hash(user.hashed_password, user_password):
            print(f"INFO: Login Failure for user {user_email}")
            return None

        print(f"INFO: Login Successful for user {user_email}")
        return user
    finally:
        session.close()


def get_user_count() -> int:
    session = db_session.create_session()
    try:
        return session.query(User).count()
    finally:
        session.close()


def find_all_users() -> list[User]:
    session = db_session.create_session()
    try:
        return session.query(User).order_by(User.name.asc()).all()
    finally:
        session.close()


def find_active_users() -> list[User]:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.active == True).order_by(User.name.asc()).all()
    finally:
        session.close()


def find_user_by_id(user_id: int) -> User | None:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        session.close()


def find_user_by_email(user_email: str) -> User | None:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.email == user_email).first()
    finally:
        session.close()


def create_user(user_name: str, user_email: str, user_password: str) -> User | None:
    if find_user_by_email(user_email):
        return None

    user = User()
    user.email = user_email
    user.name = user_name
    user.hashed_password = hash_text(user_password)
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


def edit_user(user_id: int, user_email: str = None, user_description: str = None,
              user_notification: bool = None) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.email = user_email if user_email is not None else user.email
            user.description = user_description if user_description is not None else user.description
            user.notification = user_notification if user_notification is not None else user.notification

            session.commit()

            print(f"INFO: User information changed for user {user.email}")

            return user
    finally:
        session.close()


def change_user_password(user_id: int, user_password: str) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.hashed_password = hash_text(user_password)

            session.commit()

            print(f"INFO: User password changed for user {user.email}")

            return user
    finally:
        session.close()


def delete_user(user_id: int) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.query(User).filter(User.id == user_id).delete()
            session.commit()

            print(f"INFO: User {user.email} deleted")

            return user
    finally:
        session.close()


def prepare_user(user_email: str) -> User | None:
    # check valid student account and sent out password reset mail
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.active == 1).filter(User.email == user_email).first()
        if user:
            user.reset_password = random_hash()
            session.commit()

            print(f"INFO: Reset password prepared for user {user.email}")

            return user
    finally:
        session.close()


def reset_user(user_hash_value: str, user_password: str) -> User | None:
    # check valid student account and valid password reset link
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.active == 1).filter(User.reset_password == user_hash_value).first()
        if user:
            user.hashed_password = hash_text(user_password)
            user.reset_password = ""
            session.commit()

            print(f"INFO: Password reset performed for user {user.email}")

            return user
    finally:
        session.close()


def get_all_images() -> dict:
    images = dict()
    session = db_session.create_session()
    try:
        users = session.query(User).order_by(User.name.asc()).all()

        for user in users:
            if user.image is not None and os.path.isfile(os.path.join('static/uploads/profile/', user.image)):
                images[user.id] = os.path.join('uploads/profile/', user.image)
            else:
                images[user.id] = "img/not_found.jpg"

        return images
    finally:
        session.close()


def get_user_image(user_id: int) -> str:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()

        if user.image is not None and os.path.isfile(os.path.join('static/uploads/profile/', user.image)):
            return os.path.join('uploads/profile/', user.image)
        else:
            return "img/not_found.jpg"
    finally:
        session.close()


def set_user_image(user_id: int, user_image: str) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.image = user_image

            session.commit()

            print(f"INFO: Image changed for user {user.email}")

            return user
    finally:
        session.close()
