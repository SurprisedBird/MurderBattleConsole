from enum import Enum, auto
from typing import Tuple

import message_text_config as msg
import utils
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy
from game import Game

from effects.effect import Effect


class PaymentChoice(Enum):
    HP_CHOICE = auto()
    CARD_CHOICE = auto()


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
        if isinstance(self.targets[0], Player):
            if self.activation_round == self.game.round_number:
                return False
            else:
                payment_choice = self._choose_payment()
                if payment_choice == PaymentChoice.HP_CHOICE:
                    self.targets[0].hp -= 1
                elif payment_choice == PaymentChoice.CARD_CHOICE and (
                        self.targets[0].citizen_card is not None
                        or len(self.targets[0].stolen_cards) > 0):
                    self._choose_card_payment()
        else:
            self.targets[0].citizen_card = None
        return True

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        pass

    def _choose_payment(self) -> bool:
        while (True):
            taxes_choice = self.user_interaction.read_number(
                msg.TaxesMessages.RESOLVE_PLAYER_CHOOSE_VARIANT)
            if taxes_choice == 1:
                return PaymentChoice.HP_CHOICE
            elif taxes_choice == 2 and (
                    self.targets[0].citizen_card is not None
                    or len(self.targets[0].stolen_cards) > 0):
                return PaymentChoice.CARD_CHOICE
            else:
                self.user_interaction.show_active_instant(
                    msg.Errors.CONFIRM_CHOICE)

    def _choose_card_payment(self) -> bool:
        while (True):
            cards_names = ""
            for i, card_name in enumerate(self._create_cards_names_list(),
                                          start=1):
                cards_names += (f"{i}. {card_name}\n")

            card_choice = self.user_interaction.read_number(
                f"\n{msg.PlayerMessages.CHOOSE_CARD_ACTION}\n{cards_names}")

            index = 1
            if self.targets[0].citizen_card is None:
                index == 0

            if card_choice == index:
                self.targets[0].citizen_card = None
                break

            elif card_choice is not None and card_choice in range(
                    index,
                    len(self.targets[0].stolen_cards) + 1 + index):
                del self.targets[0].stolen_cards[card_choice - 1 - index]
                break
            else:
                self.user_interaction.show_active_instant(
                    msg.Errors.CONFIRM_CHOICE)

    def _create_cards_names_list(self) -> 'List':
        cards_names_list = []
        if self.targets[0].citizen_card is not None:
            cards_names_list.append(self.targets[0].citizen_card.name)
        for card in self.targets[0].stolen_cards:
            cards_names_list.append(card.name)
        return cards_names_list
