from enum import Enum, auto
from typing import List

import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy

from effects.effect import Effect, InputStatusCode


class PaymentChoice(Enum):
    DECLINE_OPTION = auto()
    HP_OPTION = auto()
    CARD_OPTION = auto()


class WitnessEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, context.city.active_player)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.WitnessMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.city.citizens[target_number - 1])

        return True

    def _resolve_impl(self) -> bool:
        if self.activation_round == self.city.round_number:
            self.user_interaction.show_global_instant(
                msg.WitnessMessages.RESOLVE_START_PUBLICLY)
            return False

        if self.creator is self.city.active_player:
            payment_choice = self._choose_payment()
            if payment_choice == PaymentChoice.DECLINE_OPTION:
                return True
            elif payment_choice == PaymentChoice.HP_OPTION:
                self.creator.hp -= 1
                return False
            elif payment_choice == PaymentChoice.CARD_OPTION:
                card = self._choose_card()
                self._remove_card_from_target(card)
                return False

        action_effect = next((effect for effect in self.targets[0].effects
                              if utils.is_action_effect(effect)), None)

        if action_effect:
            self.user_interaction.show_global_instant(
                msg.WitnessMessages.RESOLVE_SUCCESS_PUBLICLY.format(
                    self.targets[0].name))

            self.city.active_player.hp -= 1
            self.user_interaction.show_active_instant(
                msg.WitnessMessages.RESOLVE_LOST_HP)

            action_effect.deactivate()

        return False

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(target_number,
                                                    self.city.citizens)

    def _on_clear_impl(self) -> None:
        pass

    def _create_card_list(self) -> List['Card']:
        card_list = self.creator.stolen_cards[:]

        if self.creator.citizen_card is not None:
            card_list.append(self.creator.citizen_card)

        return card_list

    def _choose_payment(self) -> PaymentChoice:
        target_has_cards = self.creator.citizen_card is not None or len(
            self.creator.stolen_cards) > 0

        payment_options = f"{msg.WitnessMessages.RESOLVE_PLAYER_CHOOSE_VARIANT}\n"
        payment_options += f"{msg.WitnessMessages.RESOLVE_PLAYER_DECLINE_OPTION}\n"
        payment_options += f"{msg.WitnessMessages.RESOLVE_PLAYER_HP_OPTION}\n"
        if target_has_cards:
            payment_options += f"{msg.WitnessMessages.RESOLVE_PLAYER_CARD_OPTION}\n"

        while (True):
            payment_choice = self.user_interaction.read_number(payment_options)

            if payment_choice == 1:
                return PaymentChoice.DECLINE_OPTION
            elif payment_choice == 2:
                return PaymentChoice.HP_OPTION
            elif payment_choice == 3 and target_has_cards:
                return PaymentChoice.CARD_OPTION
            else:
                self.user_interaction.show_active_instant(
                    msg.CommonMessages.ERROR_INVALID_OPTION)

    def _choose_card(self) -> 'Card':
        card_list = self._create_card_list()

        card_options = f"{msg.PlayerMessages.CHOOSE_CARD_ACTION}\n"
        for i, card in enumerate(card_list, start=1):
            card_options += (f"{i}. {card.name}\n")

        while (True):
            card_choice = self.user_interaction.read_number(card_options)

            if card_choice is None or \
                    (card_choice < 1) or (card_choice > len(card_list)):
                self.user_interaction.show_active_instant(
                    msg.CommonMessages.ERROR_INVALID_OPTION)
                continue

            return card_list[card_choice - 1]

    def _remove_card_from_target(self, card: 'Card') -> None:
        if self.creator.citizen_card is card:
            self.creator.citizen_card = None
        else:
            self.creator.stolen_cards.remove(card)
