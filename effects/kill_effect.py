from enum import Enum

import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy


from effects.effect import Effect, InputStatusCode


class KillEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, context.city.active_player)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.KillMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.city.citizens[target_number - 1])

        return True

    def _resolve_impl(self) -> bool:
        self.logger.info(f"Target HP before resolving = {self.targets[0].hp}")
        self.targets[0].hp -= 1
        self.logger.info(f"Target HP after resolving = {self.targets[0].hp}")

        if self.targets[0].is_alive:
            self.user_interaction.save_global(
                msg.KillMessages.RESOLVE_FAILED.format(self.targets[0].name,
                                                       self.targets[0].name))

            utils.save_message_for_player(
                self.context, self.targets[0],
                msg.KillMessages.RESOLVE_ENEMY_LOST_HP)
        else:
            self.user_interaction.save_global(
                msg.KillMessages.RESOLVE_SUCCESS.format(self.targets[0].name))

            citizen_card = self.targets[0].citizen_card

            self.logger.info(
                f"Citizen card: {self.targets[0].citizen_card.name if self.targets[0].citizen_card is not None else None}")

            if citizen_card is not None:
                self.creator.stolen_cards.append(citizen_card)
                self.targets[0].citizen_card = None
                self.user_interaction.save_active(
                    msg.StealMessages.RESOLVE_SUCCESS.format(
                        citizen_card.name))
                self.logger.info(
                    f"Stolen cards: {' '.join(card.name for card in self.creator.stolen_cards)}")
            else:
                self.user_interaction.save_active(
                    msg.KillMessages.RESOLVE_NO_CARD)

        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(
            target_number,
            self.city.citizens,
            self_as_target_allowed=False,
            creator=self.creator)

    def _on_clear_impl(self) -> None:
        pass
