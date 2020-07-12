import random
from typing import List

import user_interaction as user_inter
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy
from game import Game


class GameController:
    def __init__(self, citizens_dict, user_names) -> None:

        self.citizens_dict = citizens_dict
        self.user_names = user_names

        self.game: 'Game'

    def start_game(self):
        pass

    def prepare_game(self):
        self.game = Game()
        avilable_citizens: List['Citizen'] = []

        self._create_citizens(avilable_citizens)
        self._create_players(avilable_citizens)
        self._set_order()
        self._create_spy(avilable_citizens)
        self._show_game_state()

    def _create_citizens(self, avilable_citizens):
        for name, card in self.citizens_dict.items():
            self.game.citizens.append(Citizen(name=name, citizen_card=card))
            avilable_citizens.extend(self.game.citizens)
        user_inter.show_global_instant("Loading")

    def _create_players(self, avilable_citizens):
        # TODO: first player should not have oportunity to steal

        for user_name in self.user_names:
            random_index = random.randint(0, len(avilable_citizens) - 1)
            random_citizen = avilable_citizens.pop(random_index)

            player = Player(user_name=user_name,
                            name=random_citizen.name,
                            citizen_card=random_citizen.citizen_card)

            self.game.players.append(player)

    def _set_order(self):
        random.shuffle(self.game.players)

        user_inter.save_active("You are first player")
        user_inter.save_active("Your role is role name")
        user_inter.save_passive("Your role is role name")
        user_inter.save_global("First player is")

    def _create_spy(self, avilable_citizens):
        random_index = random.randint(0, len(avilable_citizens) - 1)
        random_citizen = avilable_citizens.pop(random_index)

        self.game.spy = Spy(name=random_citizen.name)

    def _show_game_state(self):
        user_inter.save_global("Game started")
