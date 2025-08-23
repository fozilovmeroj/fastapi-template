from random import randint


def generate_code(length: int = 6) -> int:
    return randint(10 ** length, 10 ** (length + 1) - 1)
