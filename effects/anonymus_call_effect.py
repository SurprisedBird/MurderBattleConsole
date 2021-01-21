from enum import Enum, auto
import message_text_config as msg
import utils
from citizens.citizen import Citizen
from game import Game

from effects.effect import Effect


class ErrorType(Enum):
    INVALID_TARGET = msg.AnonymousCallMessages.ERROR_INVALID_TARGET
    SELF_AS_TARGET = msg.AnonymousCallMessages.ERROR_SELF_AS_TARGET


class AnonymusCallEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 13)

    def _activate_impl(self) -> bool:
        target_number = self._read_target_number()
        self.targets.append(self.game.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.AnonymousCallMessages.ACTIVATION_SUCCESS.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        role = type(self.targets[0]).__name__
        if role == "Player":
            self.user_interaction.show_active_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_PLAYER.format(self.targets[0].name))
            self.targets[0].hp -= 1
            self.user_interaction.save_passive(
                msg.AnonymousCallMessages.RESOLVE_ENEMY_LOST_HP)
        elif role == "Spy":
            self.targets[0].hp -= 1
            self.user_interaction.show_active_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_SPY.format(self.targets[0].name))
        else:
            self.user_interaction.show_active_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_NO_SUSPECT.format(self.targets[0].name))

        return True

    def _validate(self, target_number: int) -> bool:
        is_valid = utils.validate_citizen_target_number(
            target_number, self.game.citizens)

        # Anonymus could not be set on yourself
        is_self_as_target = \
            (self.game.citizens[target_number - 1] is self.creator) \
            if is_valid else False

        if is_self_as_target:
            return (False, ErrorType.SELF_AS_TARGET)
        elif not is_valid:
            return (False, ErrorType.INVALID_TARGET)

        return (True, None)

    def _on_clear_impl(self) -> None:
        pass

    def _read_target_number(self) -> int:
        message = msg.AnonymousCallMessages.ACTIVATION_CHOOSE_TARGET
        target_number = self.user_interaction.read_number(message)

        is_valid, error_code = self._validate(target_number)
        while not is_valid:
            self.user_interaction.show_active_instant(error_code.value)
            target_number = self.user_interaction.read_number(message)
            is_valid, error_code = self._validate(target_number)

        return target_number
