from effects.effect import Effect

from typing import Type


class Card:

    def __init__(self, name: str, effect: Type[Effect]) -> None:
        self._name = name
        self._effect = effect
