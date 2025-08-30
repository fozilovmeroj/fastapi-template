from enum import Enum


class LogLevelEnum(str, Enum):
    INFO = "INFO"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
