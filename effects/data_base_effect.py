from enum import Enum
from typing import List

import message_text_config as config
import user_interaction
import utils
from citizens.citizen import Citizen
from effects.effect import Effect
from game import Game
from message_text_config import Errors


class ErrorsEnum(Enum):
    INVALID_TURGET = Errors.TARGET
    NOT_THREE_TARGET = Errors.DATA_BASE_TARGETS
    SAME_TARGETS = Errors.DATA_BASE_SAME_TARGETS


class DataBase(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, creator, 4)
        self._errors = None

    def _activate_impl(self):
        target_numbers = []
        for _ in range(3):
            target_number = user_interaction.read_index(
                config.CardTarget.ACT_DATABASE)
            target_numbers.append(target_number)

        while (not self._validate(target_numbers)):
            user_interaction.show_active_instant(self._status.value)
            target_number = user_interaction.read_index("config.type_target")
            target_numbers = []
            for _ in range(3):
                target_number = user_interaction.read_index(
                    "config.type_target")
                target_numbers.append(target_number)

        self._targets = [
            self._game.citizens[target_number - 1]
            for target_number in target_numbers
        ]
        return True

    def _validate(self, target_numbers: List[int]):

        is_in_range = [
            all(
                utils.validate_citizen_target_number(target,
                                                     self._game.citizens))
            for target in target_numbers
        ]

        if not is_in_range:
            self._status = ErrorsEnum.INVALID_TURGET
            return False

        is_three_targets = (len(target_numbers) == 3)
        if not is_three_targets:
            self._status = ErrorsEnum.NOT_THREE_TARGET
            return False

        #check if player have chosen 3 different targets
        is_different = (len(target_numbers) == len(set(target_numbers)))
        if not is_different:
            self._status = ErrorsEnum.SAME_TARGETS
            return False

        return True

    def _resolve_impl(self):
        roles = [type(target).__name__ for target in self._targets]
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
