# import logging
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List

import message_text_config as msg
from citizens.citizen import Citizen
from custom_logger import logger


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
    __priority__ = None

    def __init__(
        self,
        context: 'Context',
        name: str,
        creator: Citizen,
    ) -> None:
        self.context = context
        self.user_interaction = context.user_interaction
        self.city = self.context.city
        self.name = name
        self.creator = creator

        self.targets: List[Citizen] = []
        self.status = EffectStatus.CREATED
        self.activation_round: int
        self.logger = logger.getChild(__name__)

    def activate(self) -> None:
        if (self.status == EffectStatus.CREATED):
            is_activated = self._activate_impl()
            self.logger.info(
                f'Effect {self.name} has been activated. Current status: {self.status.name}. Target: {" ".join(target.name for target in self.targets)}'
            )

            if (is_activated):
                self.status = EffectStatus.ACTIVATED
                self.activation_round = self.city.round_number
            else:
                self.logger.warning(f'Activatoion FAILED for {self.name.name}')
                pass
        else:
            self.logger.warning(
                f'Unexpected activate call for {self.name}. Current status: {self.status.name}'
            )
            pass

    def activate_by_target(self, targets) -> None:
        is_activated = self._activate_by_target_impl(targets)
        if (self.status == EffectStatus.CREATED):

            if(is_activated):
                self.status = EffectStatus.ACTIVATED
                self.activation_round = self.city.round_number
                self.logger.info(
                    f'Effect {self.name} has been activated by target. Current status {self.status.name}'
                )
            else:
                self.logger.warning(f'Activatoion FAILED for {self.name.name}')
                pass

        else:
            self.logger.warning(
                f'Unexpected activate call for {self.name}. Current status: {self.status.name}'
            )

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
        self.logger.info(f"")
        pass

    def resolve(self) -> None:
        if (self.status == EffectStatus.ACTIVATED) or \
                (self.status == EffectStatus.RESOLVING):
            self.status = EffectStatus.RESOLVING
            is_resolved = self._resolve_impl()

            if (is_resolved):
                self.status = EffectStatus.RESOLVED
            logger.info(
                f'{self.name} Effect status changed to {self.status.name}')
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
            self.logger.info(
                f"Citizen {' '.join(target.name for target in self.targets)} effect name: {self.name}"
            )

    @abstractmethod
    def _on_clear_impl(self) -> None:
        pass

    def __lt__(self, other: 'Effect') -> bool:
        return self.__priority__ < other.__priority__

    @property
    def is_deactivated(self) -> bool:
        logger.info(f"Effect: {self.name} status: {self.status.name}")
        return self.status == EffectStatus.FINISHED

    def deactivate(self) -> None:
        # We should skip on_clear stage only
        # if resolve was not called before

        if (self.status == EffectStatus.CREATED) or \
                (self.status == EffectStatus.ACTIVATED):
            self.status = EffectStatus.FINISHED
        elif (self.status == EffectStatus.RESOLVING):
            self.status = EffectStatus.RESOLVED

        logger.info(
            f"Effect {self.name} has been deactivated. Status: {self.status.name}"
        )
