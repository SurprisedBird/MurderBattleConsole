from typing import List


class Game:
    def __init__(self) -> None:
        self.citizens: List['Citizen'] = []
        self.players: List['Player'] = []
        self.spy: 'Spy' = None
        self.round_number = 0

    @property
    def get_active_player(self) -> 'Player':
        active_player = None
        if self.round_number % 2 != 0:
            active_player = self.players[0]
        else:
            active_player = self.players[1]

        return active_player

    @property
    def get_passive_player(self) -> 'Player':
        passive_player = None
        if self.round_number % 2 == 0:
            passive_player = self.players[0]
        else:
            passive_player = self.players[1]

        return passive_player
