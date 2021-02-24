import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.player import Player
from game import Game

from effects.effect import Effect, EffectStatus, InputStatusCode


class GangEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 13)

    def _activate_impl(self) -> bool:
        self.targets.append(self.creator)
        self.user_interaction.save_active(msg.GangMessages.ACTIVATION_SUCCESS)

        return True

    def _resolve_impl(self) -> bool:
        if self.game.round_number == self.activation_round:
            return False

        for citizen in self.game.citizens:
            for effect in citizen.effects:
                if self.should_be_removed(effect):
                    citizen.effects.remove(effect)
                    self.user_interaction.save_active(
                        msg.GangMessages.RESOLVE_SUCCESS)

        return True

    def should_be_removed(self, effect: 'Effect') -> bool:
        is_current_round = (effect.activation_round == self.game.round_number)
        not_an_action = (not utils.is_action_effect(effect))

        return is_current_round and not_an_action

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        pass
