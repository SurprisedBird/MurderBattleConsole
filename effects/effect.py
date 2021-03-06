# import logging
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List

import message_text_config as msg
from citizens.citizen import Citizen
from game import Game


class EffectStatus(Enum):
    CREATED = auto()
    ACTIVATED = auto()
    RESOLVING = auto()
    RESOLVED = auto()
    FINISHED = auto()


class InputStatusCode(Enum):
    OK = msg.CommonMessages.NO_ERROR
    NOK_INVALID_TARGET = msg.CommonMessages.ERROR_INVALID_TARGET
    NOK_SELF_AS_TARGET = msg.CommonMessages.ERROR_SELF_AS_TARGET
    NOK_SAME_TARGET = msg.CommonMessages.ERROR_SAME_TARGET


class Effect(ABC):
    def __init__(self, context: 'Context', name: str, creator: Citizen,
                 priority: int) -> None:
        self.context = context
        self.user_interaction = context.user_interaction
        self.game = self.context.game
        self.name = name
        self.creator = creator
        self.priority = priority

        self.targets: List[Citizen] = []
        self.status = EffectStatus.CREATED
        self.activation_round: int

    def activate(self) -> None:
        if (self.status == EffectStatus.CREATED):
            is_activated = self._activate_impl()

            if (is_activated):
                self.status = EffectStatus.ACTIVATED
                self.activation_round = self.game.round_number
            else:
                # logging.warning(f'Actovatoion FAILED for {self._name}.')
                pass
        else:
            # logging.warning(f'Unexpected activate call for {self._name}.
            #                 Current stauts: {self._status}')
            pass

    @abstractmethod
    def _activate_impl(self) -> bool:
        """
        Setup effect's targets.

        Returns True if operation finished successfully.
        Returnd False - otherwise.
        """
        pass

    @abstractmethod
    def _validate(self, target_number: int) -> InputStatusCode:
        pass

    def resolve(self) -> None:
        if (self.status == EffectStatus.ACTIVATED) or \
            (self.status == EffectStatus.RESOLVING):
            self.status = EffectStatus.RESOLVING
            is_resolved = self._resolve_impl()

            if (is_resolved):
                self.status = EffectStatus.RESOLVED
        else:
            # logging.warning(f'Unexpected resolve call for {self._name}.
            #                 Current stauts: {self._status}')
            pass

    @abstractmethod
    def _resolve_impl(self) -> bool:
        """
        Implements core logic of each effect. It's interaction with
        other effects and game itself.

        Returns True if resolve was completed and effect should be
        removed.
        Returnd False - otherwise.
        """
        pass

    def on_clear(self) -> None:
        if self.status == EffectStatus.RESOLVED:
            self._on_clear_impl()

            self.status = EffectStatus.FINISHED

    @abstractmethod
    def _on_clear_impl(self) -> None:
        pass

    def __lt__(self, other: 'Effect') -> bool:
        return self.priority < other.priority

    def deactivate(self) -> None:
        # We should skip on_clear stage only
        # if resolve was not called before
        if (self.status == EffectStatus.CREATED) or \
            (self.status == EffectStatus.ACTIVATED):
            self.status = EffectStatus.FINISHED
        elif (self.status == EffectStatus.RESOLVING):
            self.status = EffectStatus.RESOLVED
