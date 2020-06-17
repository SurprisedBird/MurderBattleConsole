from abc import ABC

from enum import Enum

from game import Game

from citizens.citizen import Citizen

from typing import List


class EffectStatus(Enum):
    CREATED = 1
    ACTIVATED = 2
    FINISHED = 3


class Effect(ABC):

    def __init__(self, name: str, game: Game, creator: Citizen) -> None:
        self.name = name
        self.game = game
        self.targets: List[Citizen] = []
        self.creator: Citizen = creator
