from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional
import sys
from io import StringIO


class MessageScope(Enum):
    GLOBAL = auto()
    ACTIVE = auto()
    PASSIVE = auto()


class BaseUserInteraction(ABC):
    def __init__(self, context: 'Context'):
        self.context = context
        self.users = self.context.users
        self.request_numbers = []
        
        self.history = {
            MessageScope.GLOBAL: [],
            MessageScope.ACTIVE: [],
            MessageScope.PASSIVE: []            
        }

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
        self.history[MessageScope.GLOBAL].append(text)
        self._prepared_messages[MessageScope.GLOBAL].append(text)

    def save_active(self, text: str) -> None:
        self.history[MessageScope.ACTIVE].append(text)
        self._prepared_messages[MessageScope.ACTIVE].append(text)

    def save_passive(self, text: str) -> None:
        self.history[MessageScope.PASSIVE].append(text)
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
        
        if len(self.request_numbers) == 0:
            index_str = input(text)
        
            if ";" in index_str:
                for number in index_str.split(";"):
                    index = int(number)
                    self.request_numbers.append(index)
                
        if len(self.request_numbers) > 0:
            index = self.request_numbers[0]
            self.request_numbers.remove(index)
            return index
        
        if index_str.isnumeric():
            index = int(index_str)
        else:
            index = None

        return index

    def read_numbers(self, text: str = "") -> "List":
        """Reading and validating inputs.

        If input value is valid - return int
        If input value is NOT valid - return None
        """
        texts = input(text)
        self.context.action_request.parsing(texts)

        return self.context.action_request

    def is_global_empty(self):
        if not self._prepared_messages[MessageScope.GLOBAL]:
            return True
        else:
            return False
