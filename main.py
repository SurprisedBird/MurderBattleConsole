from enum import Enum, auto

from card import Card
from effects.none_effect import NoneEffect
from game_controller import GameController

citizens_dict = {
    "Охотник": Card("Ловушка", NoneEffect),
    "Врач": Card("Антидот", NoneEffect),
    "Сутенер": Card("Клофелинщица", NoneEffect)
}

user_names = ["GvinP", "Runmaget"]

if __name__ == "__main__":
    gc = GameController(citizens_dict, user_names)

    gc.start_game()
