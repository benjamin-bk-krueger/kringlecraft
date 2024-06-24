import hashlib
import os
import random
import string

from passlib.handlers.sha2_crypt import sha512_crypt as crypto


def random_hash() -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


def hash_text(text: str) -> str:
    return crypto.encrypt(text, rounds=171204)


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def file_hash(filename: str) -> str:
    return hashlib.md5(filename.encode('utf-8')).hexdigest()


def check_path(category: str, filename: str) -> bool:
    return os.path.isfile(os.path.join(f'static/uploads/{category}/', filename))


def web_path(category: str, filename: str) -> str:
    return os.path.join(f'uploads/{category}/', filename)


def dummy_path() -> str:
    return "img/not_found.jpg"


def file_ending(filename: str) -> str:
    return os.path.splitext(filename)[1][1:]
