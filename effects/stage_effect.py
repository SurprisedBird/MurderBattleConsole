from game import Game
from effects.effect import Effect
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.player import ActionType
import user_interaction
import utils


class StageEffect(Effect):
    def __init__(self, name: str, game: Game, creator: Citizen) -> None:
        Effect.__init__(self, name, game, creator)

    def activate(self) -> None:
        target_number = user_interaction.read_index('config.type_target')
        while(not self.validate(target_number)):
            user_interaction.show_active_instant("config.type_error")
            target_number = user_interaction.read_index("config.type_target")

        self.target = self.game.citizens[target_number - 1]

    def resolve(self) -> None:
        self.creator._staging_available = False
        self.creator.allowed_actions.remove(ActionType.CARD_USAGE)

        if isinstance(self.target, Player):
            self.target.hp -= 1
            user_interaction.save_passive('config.lose_hp')
            user_interaction.save_global('config.failed_stage')

        else:
            self.creator.name, self.target.name = self.target.name, self.creator.name
            self.target.hp -= 1
            if self.creator.citizen_card is not None:
                self.creator.stolen_cards.append(self.creator.citizen_card)
                self.creator.citizen_card = None

            self.creator.citizen_card = self.target.citizen_card

            creator_index, target_index = utils.find_citizen_index(
                self.game.citizens, self.creator, self.target)

            self.game.citizens[creator_index], self.game.citizens[
                target_index] = self.game.citizens[target_index], self.game.citizens[creator_index]

            user_interaction.save_global('config.citizen_die')

    def on_clear(self) -> None:
        self.creator.allowed_actions.append(ActionType.CARD_USAGE)

    def validate(self, target_number: int) -> bool:
        return (utils.validate_citizen_target_number(target_number, self.game.citizens) and self.game.citizens[target_number-1] is not self.creator)
