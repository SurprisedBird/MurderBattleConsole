from abc import ABC

from enum import Enum


class EffectStatus(Enum):
    CREATED = 1
    ACTIVATED = 2
    FINISHED = 3


class Effect(ABC):

    def __init__(self, name: str) -> None:
        self._name = name
