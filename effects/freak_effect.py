import message_text_config as msg
import utils

from effects.effect import Effect, InputStatusCode


class FreakEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: 'Citizen') -> None:
        super().__init__(context, name, creator, 12)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.DrugsMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.city.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.DrugsMessages.ACTIVATION_SUCCESS.format(self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        for effect in self.targets[0].effects:
            if type(effect).__name__ in [
                    'TrapEffect', 'AlarmEffect', 'VideocameraEffect',
                    'WitnessEffect'
            ]:
                effect.deactivate()

        self.user_interaction.save_active(
            msg.DrugsMessages.RESOLVE_SUCCESS.format(self.targets[0].name))

        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.city.citizens)

    def _on_clear_impl(self) -> None:
        pass
