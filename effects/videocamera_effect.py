import message_text_config as msg
import utils
from citizens.citizen import Citizen
from game import Game

from effects.effect import Effect, InputStatusCode
from effects.staging_effect import StagingEffect
from effects.steal_effect import StealEffect


class VideoCameraEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 8)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.VideoCameraMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.game.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.VideoCameraMessages.ACTIVATION_SUCCESS.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        if self._is_videocamera_triggered():
            enemy_name = self.game.active_player.name
            citizen_name = self.targets[0].name

            camera_message = msg.VideoCameraMessages.RESOLVE_SUCCESS.format(
                enemy_name, citizen_name)
            self.user_interaction.save_passive(camera_message)

            return True

        return False

    def _is_videocamera_triggered(self) -> bool:
        for effect in self.targets[0].effects:
            videocamera_triggered = utils.is_action_effect(effect)

            if videocamera_triggered:
                return True

        return False

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        pass
