from typing import Tuple

import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from effects.effect import Effect
from effects.steal_effect import StealEffect
from game import Game


class AlarmEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, creator, 8)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(msg.CardTarget.ACT_ALARM,
                                                 self._validate)
        self._targets.append(self._game.citizens[target_number - 1])

        user_interaction.save_active(
            msg.EffectsActivated.ACT_ALARM.format(self._targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        is_alarm_triggered, effect = self._is_alarm_triggered()

        if is_alarm_triggered:
            effect.deactivate()

            user_interaction.save_active(msg.EffectsResolved.ACT_ALARM)
            utils.save_message_for_player(self._game, self._creator,
                                          msg.EffectsResolved.PASS_ALARM)

            return True

        return False

    def _is_alarm_triggered(self) -> Tuple[bool, Effect]:
        for effect in self._targets[0].effects:
            # TODO: uncomment when KillEffect and StagingEffect will be available
            alarm_triggered = type(effect) is StealEffect  #or \
            #type(effect) is KillEffect or \
            #type(effect) is StagingEffect

            if alarm_triggered:
                return (True, effect)

        return (False, None)

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self._game.citizens)

    def _on_clear_impl(self) -> None:
        pass
