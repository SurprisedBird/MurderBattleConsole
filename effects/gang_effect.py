import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.player import Player

from effects.effect import Effect, EffectStatus, InputStatusCode


class GangEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)

    def _activate_impl(self) -> bool:
        self.targets.append(self.city)
        self.user_interaction.save_active(msg.GangMessages.ACTIVATION_SUCCESS)

        return True

    def _resolve_impl(self) -> bool:
        if self.city.round_number == self.activation_round:
            return False

        all_effects = self.city.effects[:]
        for citizen in self.city.citizens:
            all_effects.extend(citizen.effects)

        for effect in all_effects:
            if self._should_be_deactivated(effect):
                effect.deactivate()
                self.user_interaction.save_active(
                    msg.GangMessages.RESOLVE_SUCCESS)
                return True

        return True

    def _should_be_deactivated(self, effect: 'Effect') -> bool:
        is_current_round = (effect.activation_round == self.city.round_number)
        not_an_action = (not utils.is_action_effect(effect))

        return is_current_round and not_an_action

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.city.citizens)

    def _on_clear_impl(self) -> None:
        pass
