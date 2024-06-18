import random  # for captcha random numbers


def create_captcha() -> dict:
    """
    Generate a random addition captcha.

    :return: A dictionary containing the two random numbers and their sum.
    :rtype: dict
    """
    random1 = random.randint(1, 10)
    random2 = random.randint(1, 10)
    check_captcha = random1 + random2
    return {"r1": random1, "r2": random2, "res": check_captcha}
