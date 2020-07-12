from game_controller import GameController

citizens_dict = {
    "Охотник": "Ловушка",
    "Врач": "Антидот",
    "Сутенер": "Клофелинщица"
}

user_names = ["GvinP", "Runmaget"]

if __name__ == "__main__":
    gc = GameController(citizens_dict, user_names)

    gc.prepare_game()
    gc.start_game()
