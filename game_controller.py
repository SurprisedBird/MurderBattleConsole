import random

import user_interaction as user_inter
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy
from game import Game


class GameController:
    def __init__(self) -> None:

        self.citizens_dict = {
            "Охотник": "Ловушка",
            "Врач": "Антидот",
            "Сутенер": "Клофелинщица"
        }

        self.first_user = 'GvinP'
        self.second_user = 'Runmaget'
        self.available_citizens = []

    def start_game(self):
        self.game = Game()

    def prepare_game(self):
        self.create_citizens()
        self.set_order()
        self.create_player()
        self.create_spy()
        self.show_game_state()

    def create_citizens(self):
        for name, card in self.citizens_dict.items():
            self.game.citizens.append(Citizen(name=name, citizen_card=card))
            self.available_citizens.append(
                Citizen(name=name, citizen_card=card))

    def set_order(self):
        self.user_names = [self.first_user, self.second_user]
        random.shuffle(self.user_names)

    def create_player(self):
        first_player_name = self.first_user[0]
        second_player_name = self.second_user[1]

        random_citizen = self.available_citizens.pop(
            random.randint(0,
                           len(self.available_citizens) - 1))

        first_player = Player(user_name=first_player_name,
                              name=random_citizen.name,
                              citizen_card=random_citizen._citizen_card)

        random_citizen = self.available_citizens.pop(
            random.randint(0,
                           len(self.available_citizens) - 1))

        second_player = Player(user_name=second_player_name,
                               name=random_citizen.name,
                               citizen_card=random_citizen._citizen_card)

        self.game.players.append(first_player)
        self.game.first_player = first_player
        self.game.players.append(second_player)

    def create_spy(self):
        print(self.available_citizens)
        random_citizen = random.choice(self.available_citizens)

        self.game.spy = Spy(name=random_citizen.name)

    def show_game_state(self):
        pass


if __name__ == "__main__":
    print("GameController")
    gc = GameController()
    gc.start_game()
    gc.prepare_game()
