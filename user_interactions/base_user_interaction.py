from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional


class MessageScope(Enum):
    GLOBAL = auto()
    ACTIVE = auto()
    PASSIVE = auto()


class BaseUserInteraction(ABC):
    def __init__(self, context: 'Context'):
        self.context = context
        self.user_names = self.context.user_names

        self._prepared_messages = {
            MessageScope.GLOBAL: [],
            MessageScope.ACTIVE: [],
            MessageScope.PASSIVE: []
        }

    @abstractmethod
    def show_global_instant(self, text: str) -> None:
        pass

    @abstractmethod
    def show_active_instant(self, text: str) -> None:
        pass

    @abstractmethod
    def show_passive_instant(self, text: str) -> None:
        pass

    @abstractmethod
    def show_all(self) -> None:
        pass

    def save_global(self, text: str) -> None:
        self._prepared_messages[MessageScope.GLOBAL].append(text)

    def save_active(self, text: str) -> None:
        self._prepared_messages[MessageScope.ACTIVE].append(text)

    def save_passive(self, text: str) -> None:
        self._prepared_messages[MessageScope.PASSIVE].append(text)

    def _clear_messages(self) -> None:
        self._prepared_messages = {
            MessageScope.GLOBAL: [],
            MessageScope.ACTIVE: [],
            MessageScope.PASSIVE: []
        }

    def read_number(self, text: str = "") -> Optional[int]:
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

    def is_global_empty(self):
        if not self._prepared_messages[MessageScope.GLOBAL]:
            return True
        else:
            return False
