from enum import Enum, auto
from typing import List

import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy
from game import Game

from effects.effect import Effect, InputStatusCode


class PaymentChoice(Enum):
    HP_OPTION = auto()
    CARD_OPTION = auto()


class TaxesEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 14)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.TaxesMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.game.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.TaxesMessages.ACTIVATION_SUCCESS.format(self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        if self.activation_round == self.game.round_number:
            return False

        if utils.is_player(self.targets[0]):
            payment_choice = self._choose_payment()
            if payment_choice == PaymentChoice.HP_OPTION:
                self.targets[0].hp -= 1
            elif payment_choice == PaymentChoice.CARD_OPTION:
                card = self._choose_card()
                self._remove_card_from_target(card)
        else:
            if self.targets[0].citizen_card is None:
                self.targets[0].hp -= 1
            else:
                self.targets[0].citizen_card = None

        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(
            target_number,
            self.game.citizens,
            self_as_target_allowed=False,
            creator=self.creator)

    def _on_clear_impl(self) -> None:
        pass

    def _create_card_list(self) -> List['Card']:
        card_list = self.targets[0].stolen_cards[:]

        if self.targets[0].citizen_card is not None:
            card_list.append(self.targets[0].citizen_card)

        return card_list

    def _choose_payment(self) -> PaymentChoice:
        target_has_cards = self.targets[0].citizen_card is not None or len(
            self.targets[0].stolen_cards) > 0

        payment_options = f"{msg.TaxesMessages.RESOLVE_PLAYER_CHOOSE_VARIANT}\n"
        payment_options += f"{msg.TaxesMessages.RESOLVE_PLAYER_HP_OPTION}\n"
        if target_has_cards:
            payment_options += f"{msg.TaxesMessages.RESOLVE_PLAYER_CARD_OPTION}\n"

        while (True):
            payment_choice = self.user_interaction.read_number(payment_options)

            if payment_choice == 1:
                return PaymentChoice.HP_OPTION
            elif payment_choice == 2 and target_has_cards:
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
                1 > card_choice > len(self.targets[0].stolen_cards):
                self.user_interaction.show_active_instant(
                    msg.CommonMessages.ERROR_INVALID_OPTION)
                continue

            return card_list[card_choice - 1]

    def _remove_card_from_target(self, card: 'Card') -> None:
        if self.targets[0].citizen_card is card:
            self.targets[0].citizen_card = None
        else:
            self.targets[0].stolen_cards.remove(card)
