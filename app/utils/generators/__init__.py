import secrets
import string
from random import randint


def generate_code(length: int = 6) -> int:
    return randint(10 ** (length - 1), 10 ** length - 1)


def generate_password(length=12, use_special=True):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = "@$!%*?&"

    password = [
        secrets.choice(lower),
        secrets.choice(upper),
        secrets.choice(digits),
        secrets.choice(special)
    ]

    all_chars = lower + upper + digits + special
    password += [secrets.choice(all_chars) for _ in range(length - 4)]

    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
