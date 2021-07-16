import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.player import Player


from effects.effect import Effect, InputStatusCode


class AntidotEffect(Effect):
    BOOST_HP = 1000

    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.AntidoteMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.city.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.AntidoteMessages.ACTIVATION_SUCCESS.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        self.logger.info(f"Target HP before Antidot {self.targets[0].hp}")
        if self.activation_round == self.city.round_number:
            self.targets[0].hp += AntidotEffect.BOOST_HP
            self.logger.info(f"Target HP after Antidot {self.targets[0].hp}")
            return False

        if self.city.round_number == self.activation_round + 1:
            return False

        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.city.citizens)

    def _on_clear_impl(self) -> None:
        self.targets[0].hp -= AntidotEffect.BOOST_HP
        if not self.targets[0].is_alive:
            self.targets[0].hp = 1
