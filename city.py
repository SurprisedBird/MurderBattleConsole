from dataclasses import dataclass, field
from typing import List

from action_manager import ActionManager


@dataclass
class City:
    citizens: List['Citizen'] = field(default_factory=list)
    players: List['Player'] = field(default_factory=list)
    name: str = "Город"
    spy: 'Spy' = None
    round_number: int = 0
    effects: List['Effect'] = field(default_factory=list)

    @property
    def active_player(self) -> 'Player':
        active_player = None
        if self.round_number % 2 != 0:
            active_player = self.players[0]
        else:
            active_player = self.players[1]

        return active_player

    @property
    def passive_player(self) -> 'Player':
        passive_player = None
        if self.round_number % 2 == 0:
            passive_player = self.players[0]
        else:
            passive_player = self.players[1]

        return passive_player
