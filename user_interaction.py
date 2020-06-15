from enum import Enum


class MessageScope(Enum):
    GLOBAL = 1
    ACTIVE = 2
    PASSIVE = 3


class UserInteraction:

    def __init__(self) -> None:
        pass
