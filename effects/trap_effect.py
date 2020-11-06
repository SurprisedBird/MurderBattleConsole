from enum import Enum

import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy
from game import Game
from message_text_config import Errors

from effects.effect import Effect


class TrapEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, game.active_player, 0)

    def _activate_impl(self) -> bool:
        target_number = user_interaction.read_number(msg.CardTarget.ACT_TRAP)

        while (not self._validate(target_number)):
            user_interaction.show_active_instant(msg.Errors.TARGET)
            target_number = user_interaction.read_number(
                msg.CardTarget.ACT_TRAP)

        self._targets.append(self._game.citizens[target_number - 1])
        return True

    def _resolve_impl(self) -> bool:
        if self._activation_round == self._game.round_number:
            return False

        kill_steal_stage = False
        for effect in self._targets[0].effects:
            if type(effect).__name__ in [
                    "KillEffect", "StealEffect", "StageEffect"
            ]:
                kill_steal_stage = True

        if kill_steal_stage:
            user_interaction.show_global_instant(
                msg.EffectsResolved.GLOBAL_TRAP.format(
                    self._game.active_player.name))

            self._game.active_player.hp -= 1

            for effect in self._targets[0].effects:

                if type(effect).__name__ in [
                        "KillEffect", "StealEffect", "StageEffect"
                ]:
                    self._targets[0].effects.remove(effect)

            user_interaction.show_active_instant(
                msg.DayGeneral.ACT_PASS_LOST_HP)

        return True

    def _validate(self, target_number: int) -> bool:
        is_in_range_and_alive = utils.validate_citizen_target_number(
            target_number, self._game.citizens)

        if not is_in_range_and_alive:
            return False

        return True

    def _on_clear_impl(self) -> None:
        pass
