from enum import Enum
from typing import List

from card import Card
from citizens.citizen import Citizen


class ActionType(Enum):
    KILL = 1
    STEAL = 2
    STAGING = 3
    CARD_USAGE = 4


class Player(Citizen):
    def __init__(self, name: str, citizen_card: Card, hp: int = 3) -> None:
        Citizen.__init__(name, citizen_card, hp)

        self._staging_available = True
        self._stolen_cards: List[Card] = []
