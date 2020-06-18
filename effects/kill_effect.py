from game import Game
from effects.effect import Effect
from citizens.citizen import Citizen
from citizens.player import Player
import user_interaction
import utils


class KillEffect(Effect):
    def __init__(self, name: str, game: Game, creator: Citizen) -> None:
        Effect.__init__(self, name, game, creator)

    def activate(self) -> None:
        target_number = user_interaction.read_index('config.type_target')
        while(not self.validate(target_number)):
            user_interaction.show_active_instant("config.type_error")
            target_number = user_interaction.read_index("config.type_target")

        self.target = self.game.citizens[target_number - 1]

    def resolve(self) -> None:

        if isinstance(self.target, Player):
            self.target.hp -= 1
            user_interaction.save_passive('config.lose_hp')
            user_interaction.save_global('config.failed_kill')

        else:
            self.target.hp -= 1
            user_interaction.save_global('config.citizen_die')
            if self.target.citizen_card is not None:
                self.creator.stolen_cards.append(self.target.citizen_card)
                self.target.citizen_card = None
                user_interaction.save_active('config.card_stolen')
            else:
                user_interaction.save_active('config.no_card')

    def on_clear(self) -> None:
        pass

    def validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number, self.game.citizens)
