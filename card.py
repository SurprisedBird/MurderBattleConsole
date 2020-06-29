from typing import Type

from effects.effect import Effect


class Card:
    def __init__(self, name: str, effect: Type[Effect]) -> None:
        self._name = name
        self._effect = effect
