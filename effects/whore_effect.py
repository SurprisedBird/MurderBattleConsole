import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.player import Player
from game import Game

from effects.effect import Effect


class WhoreEffect(Effect):
    def __init__(self, context: 'Context', name: str, creator: Citizen) -> None:
        super().__init__(context, name, creator, 7)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.WhoreMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.game.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.WhoreMessages.ACTIVATION_SUCCESS.format(self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        if self.activation_round == self.game.round_number:
            self.user_interaction.save_global(
                msg.WhoreMessages.RESOLVE_START_PUBLICLY)

            if isinstance(self.targets[0], Player):
                self.targets[0].disable_steal_action()
                self.targets[0].disable_kill_action()
                self.targets[0].disable_staging_action()

            if self.targets[0] is self.game.passive_player:
                self.user_interaction.save_passive(
                    msg.WhoreMessages.RESOLVE_SUCCESS)

            return False

        return True

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        if isinstance(self.targets[0], Player):
            self.targets[0].enable_steal_action()
            self.targets[0].enable_kill_action()
            self.targets[0].enable_staging_action()
