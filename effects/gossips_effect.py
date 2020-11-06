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
        self.night_number = 0

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            msg.GossipsMessages.ACTIVATION_CHOOSE_TARGET, self._validate)

        self.night_number = int(target_number)
        self.targets.append(self.game.passive_player)

        return True

    def _resolve_impl(self) -> bool:
        first_action = self.game.action_manager.actions_histry[
            self.night_number][0].name

        first_targets = ""
        for target in self.game.action_manager.actions_histry[
                self.night_number][0].targets:
            first_targets += target.name + " "

        second_action = self.game.action_manager.actions_histry[
            self.night_number][1].name

        second_targets = ""
        for target in self.game.action_manager.actions_histry[
                self.night_number][1].targets:
            second_targets += target.name + " "

        user_interaction.show_active_instant(
            msg.GossipsMessages.RESOLVE_SUCCESS.format(first_action,
                                                       first_targets,
                                                       second_action,
                                                       second_targets))

        return True

    # TODO: forbid player to choose nights with own actions
    def _validate(self, target_number: int) -> bool:
        if target_number == None or target_number <= 0 or target_number > len(
                self.game.action_manager.actions_histry):
            return False

        return True

    def _on_clear_impl(self) -> None:
        pass
