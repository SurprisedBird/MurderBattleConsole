# import logging
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List

from citizens.citizen import Citizen
from game import Game


class EffectStatus(Enum):
    CREATED = auto()
    ACTIVATED = auto()
    FINISHED = auto()


class Effect(ABC):
    def __init__(self, game: Game, name: str, creator: Citizen,
                 priority: int) -> None:
        self._game = game
        self._name = name
        self._creator = creator
        self._PRIORITY = priority

        self._targets: List[Citizen] = []
        self._status = EffectStatus.CREATED
        self._activation_round: int

    def activate(self) -> None:
        if (self._status == EffectStatus.CREATED):
            is_activated = self._activate_impl()

            if (is_activated):
                self._status = EffectStatus.ACTIVATED
                self._activation_round = self._game.round_number
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
    def _validate(self, target_number: int) -> bool:
        pass

    def resolve(self) -> None:
        if (self._status == EffectStatus.ACTIVATED):
            is_finished = self._resolve_impl()

            if (is_finished):
                self._status = EffectStatus.FINISHED

        elif (self._status == EffectStatus.CREATED):
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
        if (self._status == EffectStatus.FINISHED):
            is_finished = self._on_clear_impl()

    @abstractmethod
    def _on_clear_impl(self) -> None:
        pass

    def __lt__(self, other) -> bool:
        return self._PRIORITY < other._PRIORITY

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> EffectStatus:
        return self._status

    @property
    def targets(self) -> List[Citizen]:
        return self._targets

    @property
    def priority(self) -> int:
        return self._PRIORITY
