from enum import Enum
from typing import List

import message_text_config as msg
import utils
from citizens.citizen import Citizen

from effects.effect import Effect, InputStatusCode


class DatabaseEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 6)

    def _activate_impl(self) -> bool:
        target_numbers = self._read_target_numbers()

        self.targets = [
            self.city.citizens[target_number - 1]
            for target_number in target_numbers
        ]

        return True

    def _validate(self, target_numbers: List[int]) -> InputStatusCode:
        last_target_number = target_numbers[len(target_numbers) - 1]
        if last_target_number is None or not utils.is_citizen_in_range(
                last_target_number - 1, self.city.citizens):
            return InputStatusCode.NOK_INVALID_TARGET

        # check if player have chosen 3 different targets
        contains_duplicates = (len(target_numbers) != len(set(target_numbers)))
        if contains_duplicates:
            return InputStatusCode.NOK_SAME_TARGET

        return InputStatusCode.OK

    def _resolve_impl(self) -> bool:
        self.theatre_targets_changer()

        if utils.contains_player(self.targets) and utils.contains_spy(
                self.targets):
            self.user_interaction.show_active_instant(
                msg.DatabaseMessages.RESOLVE_FIND_ALL)
        elif utils.contains_player(self.targets):
            self.user_interaction.show_active_instant(
                msg.DatabaseMessages.RESOLVE_FIND_PLAYER)
        elif utils.contains_spy(self.targets):
            self.user_interaction.show_active_instant(
                msg.DatabaseMessages.RESOLVE_FIND_SPY)
        else:
            self.user_interaction.show_active_instant(
                msg.DatabaseMessages.RESOLVE_NO_SUSPECT)

        return True

    def theatre_targets_changer(self) -> 'List':
        for effect in self.city.effects:
            if type(effect).__name__ is 'TheatreEffect':
                for i in range(0, len(self.targets)):
                    if self.targets[i] is effect.mask:
                        self.targets[i] = effect.creator
                    elif self.targets[i] is effect.creator:
                        self.targets[i] = effect.mask

        return self.targets

    def _on_clear_impl(self) -> None:
        pass

    def _read_target_numbers(self) -> List[int]:
        message = msg.DatabaseMessages.ACTIVATION_CHOOSE_TARGET

        target_numbers = []
        for _ in range(3):
            target_number = self.user_interaction.read_number(message)
            target_numbers.append(target_number)

            input_status_code = self._validate(target_numbers)
            while (input_status_code is not InputStatusCode.OK):
                target_numbers.pop()
                self.user_interaction.show_active_instant(
                    input_status_code.value)
                target_number = self.user_interaction.read_number(message)
                target_numbers.append(target_number)
                input_status_code = self._validate(target_numbers)

        return target_numbers
