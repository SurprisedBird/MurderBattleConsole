from dataclasses import dataclass
from typing import Type

from effects.effect import Effect


@dataclass
class Card:
    name: str
    effect: Type[Effect]
