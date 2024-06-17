from passlib.handlers.sha2_crypt import sha512_crypt as crypto
import kringlecraft.data.db_session as db_session
from kringlecraft.data.users import User


def hash_text(text: str) -> str:
    """Hashes a given text using a cryptographic algorithm.

    :param text: The text to be hashed.
    :return: The hashed text as a string.
    """
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    """
    :param hashed_text: The hashed text to be verified.
    :param plain_text: The plain text to compare with the hashed text.
    :return: A boolean value indicating whether the hash matches the plain text.
    """
    return crypto.verify(plain_text, hashed_text)


def login_user(email: str, password: str) -> User | None:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return None

        if not verify_hash(user.hashed_password, password):
            return None

        return user
    finally:
        session.close()


def find_user_by_id(user_id: int) -> User | None:
    """
    :param user_id: The ID of the user to find
    :return: The User object associated with the given ID, or None if no such user exists
    """
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    finally:
        session.close()
