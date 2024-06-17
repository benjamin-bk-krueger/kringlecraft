from passlib.handlers.sha2_crypt import sha512_crypt as crypto


def hash_text(text: str) -> str:
    """Hashes a given text using a cryptographic algorithm.

    :param text: The text to be hashed.
    :return: The hashed text as a string.
    """
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text
