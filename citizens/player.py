from enum import Enum, auto
from typing import Dict, List, Type

import message_text_config as msg
import user_interaction
from citizens.citizen import Citizen
from effects.effect import Effect
from effects.none_effect import NoneEffect
from effects.steal_effect import StealEffect


class ActionType(Enum):
    NONE = auto()
    STEAL = auto()
    KILL = auto()
    STAGING = auto()
    CARD_USAGE = auto()


class ActionData:
    def __init__(self, available: bool, message: str,
                 effect: Type[Effect]) -> None:
        self.available = available
        self._message = message
        self._effect = effect

    @property
    def message(self) -> str:
        return self._message

    @property
    def effect(self) -> Type[Effect]:
        return self._effect


class Player(Citizen):
    def __init__(self,
                 user_name: str,
                 name: str,
                 citizen_card: 'Card',
                 hp: int = 3) -> None:
        super().__init__(name, citizen_card, hp)

        self.user_name = user_name

        self.actions_common_list: Dict[ActionType, ActionData]
        self._init_action_common_list()

        self._allowed_actions: Dict[int, ActionData]
        self._allowed_card_actions: Dict[int, ActionData]

        self.stolen_cards: List['Card'] = []

    @property
    def is_staging_available(self):
        return self.actions_common_list[ActionType.STAGING].available

    def _init_action_common_list(self):
        self.actions_common_list = {}

        self.actions_common_list[ActionType.NONE] = ActionData(
            True, msg.UserActions.TYPE_NONE, NoneEffect)
        self.actions_common_list[ActionType.STEAL] = ActionData(
            True, msg.UserActions.TYPE_STEAL, StealEffect)
        self.actions_common_list[ActionType.KILL] = ActionData(
            True, msg.UserActions.TYPE_KILL, NoneEffect)  # TODO: change None
        self.actions_common_list[ActionType.STAGING] = ActionData(
            True, msg.UserActions.TYPE_STAGING,
            NoneEffect)  # TODO: change None
        self.actions_common_list[ActionType.CARD_USAGE] = ActionData(
            True, msg.UserActions.TYPE_CARD_USAGE, None)

    def _update_allowed_actions(self) -> None:
        self._allowed_actions = {}

        index = 0
        self._allowed_actions[index] = self.actions_common_list[
            ActionType.NONE]
        if self.actions_common_list[ActionType.STEAL].available:
            index += 1
            self._allowed_actions[index] = \
                self.actions_common_list[ActionType.STEAL]
        if self.actions_common_list[ActionType.KILL].available:
            index += 1
            self._allowed_actions[index] = \
                self.actions_common_list[ActionType.KILL]
        if self.actions_common_list[ActionType.STAGING].available:
            index += 1
            self._allowed_actions[index] = \
                self.actions_common_list[ActionType.STAGING]

    def create_action(self, game: 'Game') -> Effect:
        self._update_allowed_actions()

        user_interaction.save_active(msg.NightActionTarget.ACT_ACTION)
        for index, action_data in self._allowed_actions.items():
            message_str = msg.NightActionTarget.ACT_OPTION.format(
                index, action_data.message)

            user_interaction.save_active(message_str)

        user_interaction.show_all()

        index = user_interaction.read_number()
        while (not self._validate_action(index)):
            # TODO: add correct text to message_text_config
            index = user_interaction.read_number(msg.Errors.ACTION_CHOICE)

        # TODO: replace "Dummy_name" by actual name
        # TODO: move name initialization inside Effect class (not external)
        return self._allowed_actions[index].effect(
            game, self._allowed_actions[index].message, self)

    def _update_allowed_card_actions(self) -> None:
        self._allowed_card_actions = {}

        index = 0
        self._allowed_card_actions[index] = self.actions_common_list[
            ActionType.NONE]

        if not self.actions_common_list[ActionType.CARD_USAGE].available:
            return

        if self.citizen_card is not None:
            index += 1
            self._allowed_card_actions[index] = ActionData(
                True, self.citizen_card.name, self.citizen_card.effect
            )  # TODO: add mark in citizen card name - that it is a personal card

        for i, stolen_card in enumerate(self.stolen_cards, start=(index + 1)):
            self._allowed_card_actions[i] = ActionData(True, stolen_card.name,
                                                       stolen_card.effect)

    def create_card_action(self, game: 'Game'):
        self._update_allowed_card_actions()

        user_interaction.save_active(msg.NightActionTarget.ACT_CARD)
        for index, action_data in self._allowed_card_actions.items():
            message_str = msg.NightActionTarget.ACT_OPTION.format(
                index, action_data.message)

            user_interaction.save_active(message_str)

        user_interaction.show_all()

        index = user_interaction.read_number()
        while (not self._validate_card_action(index)):
            # TODO: add correct text to message_text_config
            index = user_interaction.read_number(msg.Errors.CARD_CHOICE)

        # TODO: replace "Dummy_name" by actual name
        # TODO: move name initialization inside Effect class (not external)
        return self._allowed_card_actions[index].effect(
            game, self._allowed_card_actions[index].message, self)

    def _validate_action(self, number: int) -> bool:
        valid = (number is not None) and \
                (number >= 0) and \
                (number < len(self._allowed_actions))
        return valid

    def _validate_card_action(self, number: int):
        valid = (number is not None) and \
                (number >= 0) and \
                (number < len(self._allowed_card_actions))
        return valid
