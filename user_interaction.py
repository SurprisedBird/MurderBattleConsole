from enum import Enum, auto
from typing import Optional


class MessageScope(Enum):
    GLOBAL = auto()
    ACTIVE = auto()
    PASSIVE = auto()


prepared_messages = {
    MessageScope.GLOBAL: [],
    MessageScope.ACTIVE: [],
    MessageScope.PASSIVE: []
}


def save_global(text: str) -> None:
    prepared_messages[MessageScope.GLOBAL].append(text)


def save_active(text: str) -> None:
    prepared_messages[MessageScope.ACTIVE].append(text)


def save_passive(text: str) -> None:
    prepared_messages[MessageScope.PASSIVE].append(text)


def show_global_instant(text: str) -> None:
    print(f"{MessageScope.GLOBAL.name}: {text}")


def show_active_instant(text: str) -> None:
    print(f"{MessageScope.ACTIVE.name}: {text}")


def show_passive_instant(text: str) -> None:
    print(f"{MessageScope.PASSIVE.name}: {text}")


def show_all() -> None:
    for scope, text_list in prepared_messages.items():
        print(f"{scope.name}:")
        for text in text_list:
            print(f"\t{text}")

    _celar_messages()


def _celar_messages() -> None:
    global prepared_messages
    prepared_messages = {
        MessageScope.GLOBAL: [],
        MessageScope.ACTIVE: [],
        MessageScope.PASSIVE: []
    }


def read_number(text: str = "") -> Optional[int]:
    """Reading and validating inputs.

    If input value is valid - return int
    If input value is NOT valid - return None
    """
    index_str = input(text)
    if index_str.isnumeric():
        index = int(index_str)
    else:
        index = None

    return index
