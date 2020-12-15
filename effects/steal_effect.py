import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from game import Game

from effects.effect import Effect


class StealEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 1)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            msg.StealMessages.ACTIVATION_CHOOSE_TARGET, self._validate)

        self.targets.append(self.game.citizens[target_number - 1])

        user_interaction.save_active(
            msg.StealMessages.ACTIVATION_SUCCESS.format(self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        citizen_card = self.targets[0].citizen_card
        if citizen_card is not None:
            self.creator.stolen_cards.append(citizen_card)
            self.targets[0].citizen_card = None
            user_interaction.save_active(
                msg.StealMessages.RESOLVE_SUCCESS.format(citizen_card.name))

            if self.targets[0] is self.game.passive_player:
                user_interaction.save_passive(
                    msg.StealMessages.RESOLVE_LOST_CARD)
        else:
            user_interaction.save_active(
                msg.StealMessages.RESOLVE_FAILED.format(self.targets[0].name))

        # user_interaction.save_global(msg.DayGeneral.GLOBAL_STEAL_CITIZEN)

        return True

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        pass
