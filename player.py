from citizen import Citizen

from card import Card

from typing import List

class Player(Citizen):

    def __init__(self, name : str, citizen_card : Card, hp : int=3) -> None:
        Citizen.__init__(name, citizen_card, hp)

        self._staging_available = True
        self._stolen_cards : List[Card] = []