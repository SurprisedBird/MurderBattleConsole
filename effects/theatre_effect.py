import message_text_config as msg
import utils
from citizens.citizen import Citizen


from effects.effect import Effect, InputStatusCode
from effects.staging_effect import StagingEffect
from effects.steal_effect import StealEffect


class TheatreEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)
        self.mask: 'Citizen'

        self.logger.getChild(__name__)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.TheatreMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.mask = self.city.citizens[target_number - 1]
        self.targets.append(self.city)

        self.user_interaction.save_active(
            msg.TheatreMessages.ACTIVATION_SUCCESS.format(
                self.mask.name))

        self.logger.info(
            f"Target name: {self.mask.name}. Creator name: {self.creator.name}.")

        return True

    def _activate_by_target_impl(self, targets) -> bool:
        citizen = self.city.citizens[targets[0] - 1]
        self.mask = citizen
        self.targets.append(self.city)

        self.user_interaction.save_active(
            msg.TheatreMessages.ACTIVATION_SUCCESS.format(
                self.mask.name))

        self.logger.info(
            f"Target name: {self.mask.name}. Creator name: {self.creator.name}.")

        return True

    def _resolve_impl(self) -> bool:
        return False

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.city.citizens)

    def _on_clear_impl(self) -> None:
        pass
