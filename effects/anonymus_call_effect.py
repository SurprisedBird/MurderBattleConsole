from enum import Enum, auto

import message_text_config as msg
import utils
from citizens.citizen import Citizen
from game import Game

from effects.effect import Effect, InputStatusCode


class AnonymusCallEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 13)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.AnonymousCallMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)

        self.targets.append(self.game.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.AnonymousCallMessages.ACTIVATION_SUCCESS.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        role = type(self.targets[0]).__name__
        if role == "Player":
            self.user_interaction.show_active_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_PLAYER.format(
                    self.targets[0].name))
            self.targets[0].hp -= 1
            self.user_interaction.save_passive(
                msg.AnonymousCallMessages.RESOLVE_ENEMY_LOST_HP)
        elif role == "Spy":
            self.targets[0].hp -= 1
            self.user_interaction.show_active_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_SPY.format(
                    self.targets[0].name))
        else:
            self.user_interaction.show_active_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_NO_SUSPECT.
                format(self.targets[0].name))

        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(
            target_number,
            self.game.citizens,
            self_as_target_allowed=False,
            creator=self.creator)

    def _on_clear_impl(self) -> None:
        pass
