import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from effects.effect import Effect
from game import Game


class StealEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, creator, 1)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            msg.NightActionTarget.ACT_STEAL, self._validate)

        self.targets.append(self.game.citizens[target_number - 1])

        user_interaction.save_active(
            msg.NightActionTarget.ACT_STEAL_ACTIVATED.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        citizen_card = self.targets[0].citizen_card
        if citizen_card is not None:
            self.creator.stolen_cards.append(citizen_card)
            self.targets[0].citizen_card = None
            user_interaction.save_active(
                msg.NightResult.ACT_STEAL_SUCCESSFULL.format(
                    citizen_card.name))

            if self.targets[0] is self.game.passive_player:
                user_interaction.save_passive(msg.NightResult.PASS_LOST_CARD)
        else:
            user_interaction.save_active(
                msg.NightResult.ACT_STEAL_UNSUCCESSFULL.format(
                    self.targets[0].name))

        user_interaction.save_global(msg.DayGeneral.GLOBAL_STEAL_CITIZEN)

        return True

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        pass
