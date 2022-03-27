from typing import Tuple

import message_text_config as msg
import utils
from citizens.citizen import Citizen


from effects.effect import Effect, InputStatusCode

# Should have the lower priority than most part of effect (e.g. AnonymusCall)


class SpyEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)

    def _activate_impl(self) -> bool:
        self.targets.append(self.city.spy)
        return True

    def _resolve_impl(self) -> bool:
        is_spy_triggered, effect = self._is_spy_triggered()

        if is_spy_triggered:
            effect.creator.hp -= 1
            citizen_card = self.city.spy.citizen_card
            effect.creator.stolen_cards.append(citizen_card)
            self.city.spy.citizen_card = None
            self.user_interaction.save_active(
                msg.StealMessages.RESOLVE_SUCCESS.format(citizen_card.name))

            self.city.spy.hp = 0

            effect.deactivate()
            self.logger.info(
                f"Effect on spy: {effect.name}, effect status {effect.status.name}")

            self.user_interaction.show_active_instant(
                msg.SpyMessages.RESOLVE_LOST_HP)

        if not self.city.spy.is_alive:
            self.user_interaction.show_global_instant(
                msg.SpyMessages.RESOLVE_ATTACK_SPY.format(
                    self.targets[0].name, self.targets[0].name))
            return True

        return False

    def _is_spy_triggered(self) -> Tuple[bool, Effect]:
        for effect in self.targets[0].effects:
            spy_triggered = utils.is_action_effect(
                effect) and not effect.is_deactivated

            self.logger.info(
                f"Effect on spy: {effect.name}, effect status {effect.status.name}")

            if spy_triggered:
                return (True, effect)

        return (False, None)

    def _validate(self, target_number: int) -> InputStatusCode:
        return InputStatusCode.OK

    def _on_clear_impl(self) -> None:
        pass
