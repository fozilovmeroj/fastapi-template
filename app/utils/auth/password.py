import re

"""
    Requirements
    - min length: 8
    - at least one special character
    - at least one lowercase letter
    - at least one uppercase letter
    - at least one digit
"""
password_regex = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)


def validate_password(password: str) -> bool:
    return bool(password_regex.match(password))
