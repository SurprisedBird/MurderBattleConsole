from typing import Type

from effects.effect import Effect


class Card:
    def __init__(self, name: str, effect: Type[Effect]) -> None:
        self.name = name
        self.effect = effect
