import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from effects.effect import Effect
from effects.steal_effect import StealEffect
from game import Game


class VideoCameraEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, creator, 6)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(msg.CardTarget.ACT_CAMERA,
                                                 self._validate)
        self._targets.append(self._game.citizens[target_number - 1])

        user_interaction.save_active(
            msg.EffectsActivated.ACT_CAMERA.format(self._targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        if self._is_videocamera_triggered():
            enemy_name = self._game.active_player.name
            citizen_name = self._targets[0].name

            camera_message = msg.EffectsResolved.PASS_CAMERA.format(
                enemy_name, citizen_name)
            user_interaction.save_passive(camera_message)

            return True

        return False

    def _is_videocamera_triggered(self) -> bool:
        for effect in self._targets[0].effects:
            # TODO: uncomment when KillEffect and StagingEffect will be available
            videocamera_triggered = type(effect) is StealEffect  #or \
            #type(effect) is KillEffect or \
            #type(effect) is StagingEffect

            # Check that videocamera was triggered
            # not by camera creator
            videocamera_triggered = videocamera_triggered and \
                (effect._creator is not self._creator)

            if videocamera_triggered:
                return True

        return False

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self._game.citizens)

    def _on_clear_impl(self) -> None:
        pass
