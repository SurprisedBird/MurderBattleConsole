from effects.effect import Effect
from card import Card

from typing import List


class Citizen:

    def __init__(self, name: str, citizen_card: Card, hp: int = 1) -> None:
        self._name = name
        self._hp = hp
        self._citizen_card = citizen_card
        self._effects: List[Effect] = []

    @property
    def is_alive(self) -> bool:
        return self._hp > 0
