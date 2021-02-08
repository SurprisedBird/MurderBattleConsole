import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.player import Player
from game import Game

from effects.effect import Effect, EffectStatus


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

        card_effects = []
        citizens = self.context.game.citizens

        for citizen in citizens:
            card_effect = next(
                (effect
                 for effect in citizen.effects if self.is_crad_effect(effect)),
                None)

            if card_effect: card_effects.append(card_effect)

        for effect in card_effects:
            effect.deactivate()
            self.user_interaction.save_active(msg.GangMessages.RESOLVE_SUCCESS)

        return True

    def is_crad_effect(self, effect):
        is_next_round = (effect.activation_round == self.activation_round + 1)
        not_an_action = (not utils.is_action_effect(effect))

        return is_next_round and not_an_action

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        pass
