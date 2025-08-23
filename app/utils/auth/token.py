from datetime import datetime, timedelta


def default_token_expiry() -> datetime:
    return datetime.now() + timedelta(days=1)


def default_code_expiry() -> datetime:
    return datetime.now() + timedelta(minutes=10)
