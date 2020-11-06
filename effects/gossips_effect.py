from enum import Enum
from typing import List

import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from game import Game
from message_text_config import Errors

from effects.effect import Effect


class GossipsEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, creator, 4)
        self._errors = None
        self.night_number = 0

    def _activate_impl(self):
        target_number = user_interaction.read_number(
            msg.EffectsActivated.ACT_GOSSIPS)
        while (not self._validate(target_number)):
            user_interaction.show_active_instant(Errors.TARGET)
            target_number = user_interaction.read_number(
                msg.EffectsActivated.ACT_GOSSIPS)

        self.night_number = int(target_number)
        self._targets.append(self._game.passive_player)

        return True

    def _validate(self, target_number: int):
        if target_number == None or target_number <= 0 or target_number > len(
                self._game.action_manager.actions_histry):
            return False

        return True

    def _resolve_impl(self):
        first_action = self._game.action_manager.actions_histry[
            self.night_number][0].name

        first_targets = ""
        for target in self._game.action_manager.actions_histry[
                self.night_number][0]._targets:
            first_targets += target.name + " "

        second_action = self._game.action_manager.actions_histry[
            self.night_number][1].name

        second_targets = ""
        for target in self._game.action_manager.actions_histry[
                self.night_number][1]._targets:
            second_targets += target.name + " "

        user_interaction.show_active_instant(
            f"В эту ночь убийца совершил следующие действия:\n {first_action}, цель: {first_targets}\n {second_action}, цель: {second_targets}"
        )

        return True

    def _on_clear_impl(self):
        pass
