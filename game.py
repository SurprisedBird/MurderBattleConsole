from typing import List

from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy


class Game:
    def __init__(self) -> None:
        self.citizens: List[Citizen] = []
        self.player: List[Player] = []
        self.spy: Spy = None
        self.first_player: Player = None
        self.round_number = 0

    def get_active_player(self) -> Player:
        pass

    def get_passive_player(self) -> Player:
        pass
