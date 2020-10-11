from enum import Enum
from typing import List, Tuple

import message_text_config as config
import user_interaction
import utils
from citizens.citizen import Citizen
from game import Game
from message_text_config import Errors

from effects.effect import Effect


class ErrorType(Enum):
    INVALID_TURGET = Errors.TARGET
    SAME_TARGETS = Errors.DATA_BASE_SAME_TARGETS
    # NOT_THREE_TARGET = Errors.DATA_BASE_TARGETS


class DatabaseEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, creator, 4)

    def _activate_impl(self) -> bool:
        target_numbers = self._read_target_numbers()

        self.targets = [
            self.game.citizens[target_number - 1]
            for target_number in target_numbers
        ]

        return True

    def _validate(self, target_numbers: List[int]) -> Tuple[bool, ErrorType]:
        last_target_number = target_numbers[len(target_numbers) - 1]
        if last_target_number is None or not utils.is_citizen_in_range(
                last_target_number - 1, self.game.citizens):
            return False, ErrorType.INVALID_TURGET

        #check if player have chosen 3 different targets
        contains_duplicates = (len(target_numbers) != len(set(target_numbers)))
        if contains_duplicates:
            return False, ErrorType.SAME_TARGETS

        return True, None

    def _resolve_impl(self) -> bool:
        roles = [type(target).__name__ for target in self.targets]
        if ("Player" in roles) and ("Spy" in roles):
            user_interaction.show_active_instant(
                config.EffectsResolved.ACT_DATABASE_FIND_ALL)
        elif "Player" in roles:
            user_interaction.show_active_instant(
                config.EffectsResolved.ACT_DATABASE_FIND_PLAYER)
        elif "Spy" in roles:
            user_interaction.show_active_instant(
                config.EffectsResolved.ACT_DATABASE_FIND_SPY)
        else:
            user_interaction.show_active_instant(
                config.EffectsResolved.ACT_DATABASE_NO_SUSPECT)

        return True

    def _on_clear_impl(self) -> None:
        pass

    def _read_target_numbers(self) -> List[int]:
        message = config.CardTarget.ACT_DATABASE

        target_numbers = []
        for _ in range(3):
            target_number = user_interaction.read_number(message)
            target_numbers.append(target_number)

            is_valid, error_code = self._validate(target_numbers)
            while not is_valid:
                target_numbers.pop()
                user_interaction.show_active_instant(error_code.value)
                target_number = user_interaction.read_number(message)
                target_numbers.append(target_number)
                is_valid, error_code = self._validate(target_numbers)

        return target_numbers
