from enum import Enum
from typing import List

import message_text_config as msg
import utils
from citizens.citizen import Citizen


from effects.effect import Effect, InputStatusCode


class GossipsEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)
        self.night_number = 0

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.GossipsMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)

        self.night_number = int(target_number)
        self.targets.append(self.city.passive_player)

        return True

    def _resolve_impl(self) -> bool:
        first_action_effect = self.context.action_manager.actions_history[self.night_number][0]
        first_action = first_action_effect.name

        first_targets = ""
        for target in self.context.action_manager.actions_history[
                self.night_number][0].targets:
            if type(first_action_effect).__name__ == "StagingEffect":
                target.name = first_action_effect.creator.name
            first_targets += target.name + " "

        second_action_effect = self.context.action_manager.actions_history[self.night_number][1]
        second_action = second_action_effect.name

        second_targets = ""
        for target in self.context.action_manager.actions_history[
                self.night_number][1].targets:
            second_targets += target.name + " "

        self.logger.info(
            f"First action = {first_action}, second action = {second_action} first target = {first_targets}, second target = {second_targets}")

        self.user_interaction.show_active_instant(
            msg.GossipsMessages.RESOLVE_SUCCESS.format(first_action,
                                                       first_targets,
                                                       second_action,
                                                       second_targets))

        return True

    # TODO: forbid player to choose nights with own actions
    def _validate(self, target_number: int) -> InputStatusCode:
        if target_number == None or target_number <= 0 or target_number > len(
                self.context.action_manager.actions_history):
            return InputStatusCode.NOK_INVALID_TARGET

        return InputStatusCode.OK

    def _on_clear_impl(self) -> None:
        pass
