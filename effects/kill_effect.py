from enum import Enum
from typing import Tuple

import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy
from game import Game
from message_text_config import Errors

from effects.effect import Effect


class ErrorType(Enum):
    INVALID_TARGET = msg.KillMessages.ERROR_INVALID_TARGET
    SELF_AS_TARGET = msg.KillMessages.ERROR_SELF_AS_TARGET


class KillEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, context.game.active_player, 0)

    def _activate_impl(self) -> bool:
        target_number = self._read_target_number()
        self.targets.append(self.game.citizens[target_number - 1])

        return True

    def _resolve_impl(self) -> bool:
        self.targets[0].hp -= 1

        if self.targets[0].is_alive:
            self.user_interaction.save_global(
                msg.KillMessages.RESOLVE_FAILED.format(self.targets[0].name,
                                                       self.targets[0].name))

            utils.save_message_for_player(
                self.context, self.targets[0],
                msg.KillMessages.RESOLVE_ENEMY_LOST_HP)
        else:
            self.user_interaction.save_global(
                msg.KillMessages.RESOLVE_SUCCESS.format(self.targets[0].name))

            citizen_card = self.targets[0].citizen_card
            if citizen_card is not None:
                self.creator.stolen_cards.append(citizen_card)
                self.targets[0].citizen_card = None
                self.user_interaction.save_active(
                    msg.StealMessages.RESOLVE_SUCCESS.format(
                        citizen_card.name))
            else:
                self.user_interaction.save_active(
                    msg.KillMessages.RESOLVE_NO_CARD)

        return True

    def _validate(self, target_number: int) -> Tuple[bool, ErrorType]:
        is_valid = utils.validate_citizen_target_number(
            target_number, self.game.citizens)

        # Kill could not be set on yourself
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

    # TODO: duplicating logic. There are seveal places in code with same read and validate logic
    # Fix duplication AND\OR make error codes returnal - common practice for every effect
    def _read_target_number(self) -> int:
        message = msg.KillMessages.ACTIVATION_CHOOSE_TARGET
        target_number = self.user_interaction.read_number(message)

        is_valid, error_code = self._validate(target_number)
        while not is_valid:
            self.user_interaction.show_active_instant(error_code.value)
            target_number = self.user_interaction.read_number(message)
            is_valid, error_code = self._validate(target_number)

        return target_number
