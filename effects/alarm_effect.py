from typing import Tuple

import message_text_config as msg
import utils
from citizens.citizen import Citizen

from effects.effect import Effect, InputStatusCode


class AlarmEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.AlarmMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.city.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.AlarmMessages.ACTIVATION_SUCCESS.format(self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        is_alarm_triggered, effect = self._is_alarm_triggered()

        if is_alarm_triggered:
            effect.deactivate()

            self.user_interaction.save_active(
                msg.AlarmMessages.RESOLVE_FORCED_TO_RUN)
            utils.save_message_for_player(
                self.context, self.creator,
                msg.AlarmMessages.RESOLVE_ALARM_ACTIVATED)

            return True

        return False

    def _is_alarm_triggered(self) -> Tuple[bool, Effect]:
        for effect in self.targets[0].effects:
            alarm_triggered = utils.is_action_effect(effect)

            if alarm_triggered:
                return (True, effect)

        return (False, None)

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.city.citizens)

    def _on_clear_impl(self) -> None:
        pass
