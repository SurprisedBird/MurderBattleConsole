from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Dict, List, Type

import message_text_config as msg
import user_interaction
from card import Card
from effects.effect import Effect
from effects.kill_effect import KillEffect
from effects.none_effect import NoneEffect
from effects.staging_effect import StagingEffect
from effects.steal_effect import StealEffect

from citizens.citizen import Citizen


class ActionType(Enum):
    NONE = auto()
    STEAL = auto()
    KILL = auto()
    STAGING = auto()
    CARD_USAGE = auto()


@dataclass
class ActionData:
    available: bool
    card: Card

    @property
    def name(self) -> Effect:
        return self.card.name

    @property
    def effect(self) -> Effect:
        return self.card.effect


class Player(Citizen):
    def __init__(self,
                 user_name: str,
                 name: str,
                 citizen_card: Card,
                 hp: int = 3) -> None:
        super().__init__(name, citizen_card, hp)

        self.user_name = user_name
        self.stolen_cards: List[Card] = []

        self.actions_common_list: Dict[ActionType, ActionData]
        self._init_action_common_list()

        self._allowed_actions: Dict[int, ActionData]
        self._allowed_card_actions: Dict[int, ActionData]

        # TODO: Figure out how to remove this ugly logic
        # Player can't use staging if he used staging earlier
        self.staging_was_used = False
        # If staging was chosen as action - card action
        # could not be performed on this turn
        self._staging_processing = False

        self._chosen_card: Card

    def _init_action_common_list(self):
        self.actions_common_list = {}

        create_action_data = lambda message, effect: ActionData(
            True, Card(message, effect))
        self.actions_common_list[ActionType.NONE] = \
            create_action_data(msg.PlayerMessages.ACTION_NONE, NoneEffect)
        self.actions_common_list[ActionType.STEAL] = \
            create_action_data(msg.PlayerMessages.ACTION_STEAL, StealEffect)
        self.actions_common_list[ActionType.KILL] = \
            create_action_data(msg.PlayerMessages.ACTION_KILL, KillEffect)
        self.actions_common_list[ActionType.STAGING] = \
            create_action_data(msg.PlayerMessages.ACTION_STAGING, StagingEffect)
        self.actions_common_list[ActionType.CARD_USAGE] = \
            create_action_data(msg.PlayerMessages.ACTION_CARD_USAGE, None)

# =================================================================
# Utility functions
# =================================================================

    def _show_available_options(
            self, message: str, allowed_options: Dict[int,
                                                      ActionData]) -> None:
        user_interaction.save_active(message)
        for index, action_data in allowed_options.items():
            message_str = msg.PlayerMessages.OPTION.format(
                index, action_data.name)

            user_interaction.save_active(message_str)

        user_interaction.show_all()

    def _read_chosen_option(self, error_message: str,
                            validate_method: Callable[[int], bool]) -> int:
        index = user_interaction.read_number()
        while (not validate_method(index)):
            index = user_interaction.read_number(error_message)

        return index

# =================================================================
# Create action
# =================================================================

    def create_action(self, game: 'Game') -> Effect:
        self._update_allowed_actions()

        self._show_available_actions()

        index = self._read_chosen_action()

        effect = self._allowed_actions[index].effect
        action = effect(game, self._allowed_actions[index].name, self)

        self._staging_processing = effect is StagingEffect

        return action

    def disable_used_staging(self) -> None:
        # Disable staging forever if it was used
        if self._staging_processing:
            self.disable_staging_action()
            self.staging_was_used = True
            self._staging_processing = False

    def _show_available_actions(self) -> None:
        self._show_available_options(msg.PlayerMessages.CHOOSE_ACTION,
                                     self._allowed_actions)

    def _read_chosen_action(self) -> int:
        return self._read_chosen_option(msg.PlayerMessages.ERROR_ACTION_CHOICE,
                                        self._validate_action)

    def _update_allowed_actions(self) -> None:
        self._allowed_actions = {}

        index = 0
        for action_type, action_data in self.actions_common_list.items():
            if action_data.available and \
                (action_type is not ActionType.CARD_USAGE):
                self._allowed_actions[index] = action_data
                index += 1

    def _validate_action(self, number: int) -> bool:
        valid = (number is not None) and \
                (number >= 0) and \
                (number < len(self._allowed_actions))
        return valid

# =================================================================
# Create card action
# =================================================================

    def create_card_action(self, game: 'Game'):
        self._update_allowed_card_actions()

        self._show_available_card_actions()

        index = self._read_chosen_card_action()

        self._chosen_card = self._allowed_card_actions[index].card
        effect = self._chosen_card.effect
        action = effect(game, self._allowed_card_actions[index].name, self)
        return action

    def remove_used_card(self) -> None:
        if self._chosen_card is self.citizen_card:
            self.citizen_card = None
        elif self._chosen_card in self.stolen_cards:
            self.stolen_cards.remove(self._chosen_card)

        self._chosen_card = None

    def _show_available_card_actions(self) -> None:
        self._show_available_options(msg.PlayerMessages.CHOOSE_CARD_ACTION,
                                     self._allowed_card_actions)

    def _read_chosen_card_action(self) -> int:
        return self._read_chosen_option(
            msg.PlayerMessages.ERROR_CARD_ACTION_CHOICE,
            self._validate_card_action)

    def _update_allowed_card_actions(self) -> None:
        self._allowed_card_actions = {}

        index = 0
        self._allowed_card_actions[index] = \
            self.actions_common_list[ActionType.NONE]

        if self.actions_common_list[ActionType.CARD_USAGE].available \
                and not self._staging_processing:

            if self.citizen_card is not None:
                index += 1
                self._allowed_card_actions[index] = \
                    ActionData(True, self.citizen_card)

            for i, stolen_card in enumerate(self.stolen_cards,
                                            start=(index + 1)):
                self._allowed_card_actions[i] = ActionData(True, stolen_card)

    def _validate_card_action(self, number: int):
        valid = (number is not None) and \
                (number >= 0) and \
                (number < len(self._allowed_card_actions))
        return valid


# =================================================================
# Available options management
# =================================================================

    def disable_steal_action(self) -> None:
        self.actions_common_list[ActionType.STEAL].available = False

    def disable_kill_action(self) -> None:
        self.actions_common_list[ActionType.KILL].available = False

    def disable_staging_action(self) -> None:
        self.actions_common_list[ActionType.STAGING].available = False

    def disable_card_usage_action(self) -> None:
        self.actions_common_list[ActionType.CARD_USAGE].available = False

    def enable_steal_action(self) -> None:
        self.actions_common_list[ActionType.STEAL].available = True

    def enable_kill_action(self) -> None:
        self.actions_common_list[ActionType.KILL].available = True

    def enable_staging_action(self) -> None:
        if (not self.staging_was_used):
            self.actions_common_list[ActionType.STAGING].available = True

    def enable_card_usage_action(self) -> None:
        self.actions_common_list[ActionType.CARD_USAGE].available = True
