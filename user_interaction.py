from enum import Enum
from typing import Optional

# TODO: implement user_interaction as a class. And pass instance of this class\
# to every effect as argument


class MessageScope(Enum):
    GLOBAL = 1
    ACTIVE = 2
    PASSIVE = 3


prepared_messages = {MessageScope.GLOBAL: [],
                     MessageScope.ACTIVE: [], MessageScope.PASSIVE: []}


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
        print(f"{scope.name}: {text_list}")
    prepared_messages.clear()


def read_index(text: str) -> Optional[int]:
    """Reading and validating inputs.

    If input value is valid - return int
    If input value is NOT valid - return None
    """
    index = input(text)
    if index.isnumeric():
        index = int(text)
    else:
        index = None

    return index
