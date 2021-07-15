import message_text_config as msg
import utils
from citizens.citizen import Citizen

from effects.effect import Effect, InputStatusCode
from effects.staging_effect import StagingEffect
from effects.steal_effect import StealEffect


class VideoCameraEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.VideoCameraMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.city.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.VideoCameraMessages.ACTIVATION_SUCCESS.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        triggered_effect = self._is_videocamera_triggered()
        if triggered_effect is not None:
            if self.theatre_name() is not None:
                enemy_name = self.theatre_name()
            else:
                enemy_name = triggered_effect.creator.name

            citizen_name = self.targets[0].name

            camera_message = msg.VideoCameraMessages.RESOLVE_SUCCESS.format(
                enemy_name, citizen_name)

            utils.save_message_for_player(
                self.context, self.creator, camera_message)
            self.user_interaction.show_all()

            return True

        return False

    def theatre_name(self) -> str:
        for effect in self.city.effects:
            if type(effect).__name__ is 'TheatreEffect':
                if self._is_videocamera_triggered().creator is effect.creator:
                    return effect.mask.name
        return None

    def _is_videocamera_triggered(self) -> 'Effect':
        for effect in self.targets[0].effects:
            videocamera_triggered = utils.is_action_effect(effect)

            if videocamera_triggered:
                self.logger.info(f"Videocamera was triggered by {effect.name}")
                return effect

        return None

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.city.citizens)

    def _on_clear_impl(self) -> None:
        pass
