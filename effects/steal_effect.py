from game import Game
from effects.effect import Effect
from citizens.citizen import Citizen
import user_interaction
import utils


class StealEffect(Effect):

    def __init__(self, name: str, game: Game, creator: Citizen) -> None:
        Effect.__init__(self, name, game, creator)

    def activate(self):
        target_number = user_interaction.read_index("config.type_target")
        while(not self.validate(target_number)):
            user_interaction.show_active_instant("config.type_error")
            target_number = user_interaction.read_index("config.type_target")

        self.target = self.game.citizens[target_number - 1]

    def resolve(self):
        if self.targets[0].citizen_card is not None:

            self.creator.stolen_cards.append(self.targets[0].citizen_card)
            self.targets[0].citizen_card = None
            user_interaction.save_active("config.card_stolen")

            if self.target is self.game.get_passive_player():
                user_interaction.save_passive("config.lost_card")

        else:
            user_interaction.save_active("config.no_card")

    def validate(self, target_number):
        return utils.validate_citizen_target_number(target_number, self.game.citizens)
