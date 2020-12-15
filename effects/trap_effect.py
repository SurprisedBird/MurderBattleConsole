from enum import Enum

import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy
from game import Game
from message_text_config import Errors

from effects.effect import Effect


class TrapEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, self.context.game.active_player, 8)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            msg.TrapMessages.ACTIVATION_CHOOSE_TARGET, self._validate)

        self.targets.append(self.game.citizens[target_number - 1])
        return True

    def _resolve_impl(self) -> bool:
        if self.activation_round == self.game.round_number:
            return False

        action_effect = next((effect for effect in self.targets[0].effects
                              if utils.is_action_effect(effect)), None)

        if action_effect:
            user_interaction.show_global_instant(
                msg.TrapMessages.RESOLVE_SUCCESS.format(self.targets[0].name))

            self.game.active_player.hp -= 1

            action_effect.deactivate()

            user_interaction.show_active_instant(
                msg.TrapMessages.RESOLVED_CATCHED)

        return True

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        pass
