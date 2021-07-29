from abc import ABC, abstractmethod


class Context(ABC):
    @property
    @abstractmethod
    def users(self):
        pass

    @property
    @abstractmethod
    def user_interaction(self):
        pass

    @property
    @abstractmethod
    def city(self):
        pass

    @property
    @abstractmethod
    def action_manager(self):
        pass
