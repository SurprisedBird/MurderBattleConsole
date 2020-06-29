import user_interaction
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy
from effects.effect import Effect
from game import Game


class StealEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        Effect.__init__(self, game, name, creator, 0)

    def _activate_impl(self) -> bool:
        target_number = user_interaction.read_number("config.type_target")
        while (not self._validate(target_number)):
            user_interaction.show_active_instant("config.type_error")
            target_number = user_interaction.read_number("config.type_target")

        self._targets.append(self._game.citizens[target_number - 1])

        return True

    def _resolve_impl(self) -> bool:
        if self._targets[0].citizen_card is not None:
            self._creator.stolen_cards.append(self._targets[0].citizen_card)
            self._targets[0].citizen_card = None
            user_interaction.save_active("config.card_stolen")
            user_interaction.save_passive("config.lost_card")

        else:
            user_interaction.save_active("config.no_card")

        return True

    def _validate(self, target_number: int):
        return utils.validate_citizen_target_number(target_number,
                                                    self._game.citizens)

    def on_clear(self) -> None:
        pass
