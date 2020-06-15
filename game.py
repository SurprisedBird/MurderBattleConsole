from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy

from typing import List


class Game:

    def __init__(self) -> None:
        self.citizens: List[Citizen] = []
        self.player: List[Player] = []
        self.spy: Spy = None
        self.first_player: Player = None
        self.round_number = 0
