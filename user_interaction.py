from enum import Enum


class MessageScope(Enum):
    GLOBAL = 1
    ACTIVE = 2
    PASSIVE = 3


def save_global(text: str) -> None:
    pass


def save_active(text: str) -> None:
    pass


def save_passive(text: str) -> None:
    pass


def show_active_instant(text: str) -> None:
    print(text)


def read_index(text: str) -> int:
    """Reading and validating inputs.

    If input value is valid - return int
    If input value is NOT valie - return None
    """
    return 0
