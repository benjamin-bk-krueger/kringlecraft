import random
import string
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
import kringlecraft.data.db_session as db_session
from kringlecraft.utils.mail_tools import send_mail
from kringlecraft.data.users import User


def random_hash() -> str:
    """
    Generate a random hash.

    :return: A randomly generated hash string.
    :rtype: str
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


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


def login_user(user_email: str, user_password: str) -> User | None:
    """
    Login User

    :param user_email: The email address of the user.
    :param user_password: The password of the user.
    :return: The logged-in user object of type `User` if successful, otherwise `None`.

    """
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.email == user_email).first()
        if not user:
            print(f"Login Failure for user {user_email}")
            return None

        if not verify_hash(user.hashed_password, user_password):
            print(f"Login Failure for user {user_email}")
            return None

        print(f"Login Successful for user {user_email}")
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


def prepare_user(user_email: str, www_link: str) -> User | None:
    """
    :param user_email: The email of the user for whom the password reset is being prepared.
    :param www_link: The base URL of the website to which the password reset link will be appended.
    :return: The User object representing the user for whom the password reset is being prepared. Returns None if no active user with the given email is found.

    Prepares a user for password reset by generating a random password reset hash, updating the user's reset_password field, and sending a password reset email with the password reset link.
    """
    # check valid student account and sent out password reset mail
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.active == 1).filter(User.email == user_email).first()
        if user:
            user.reset_password = random_hash()
            session.commit()

            recipients = list()
            recipients.append(user_email)
            body_text = f"Reset your password here: {www_link}/reset/{user.reset_password}"
            send_mail("Password Reset Link", body_text, recipients)

            return user
    finally:
        session.close()


def reset_user(user_hash: str, user_password: str) -> User | None:
    """
    Reset the password of a user.

    :param user_hash: The reset password hash.
    :param user_password: The new password for the user.
    :return: The User object if successful, None if the password reset failed.
    """
    # check valid student account and valid password reset link
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.active == 1).filter(User.reset_password == user_hash).first()
        if user:
            user.hashed_password = hash_text(user_password)
            user.reset_password = ""
            session.commit()

            print(f"Password Reset for user {user.email}")
            recipients = list()
            recipients.append(user.email)
            send_mail(f"{user.name} - Password Reset", "Your password has been reset.", recipients)

            return user
    finally:
        session.close()
