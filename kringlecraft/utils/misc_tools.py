import random  # for captcha random numbers
import string

from passlib.handlers.sha2_crypt import sha512_crypt as crypto


def create_captcha() -> dict:
    random1 = random.randint(1, 10)
    random2 = random.randint(1, 10)
    check_captcha = random1 + random2
    return {"r1": random1, "r2": random2, "res": check_captcha}


def random_hash() -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))


def hash_text(text: str) -> str:
    return crypto.encrypt(text, rounds=171204)


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


