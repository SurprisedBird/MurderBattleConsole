from typing import List

from action_manager import ActionManager


class Game:
    def __init__(self) -> None:
        self.citizens: List['Citizen'] = []
        self.players: List['Player'] = []
        self.spy: 'Spy' = None
        self.round_number = 0
        self.action_manager: ActionManager

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
