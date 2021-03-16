from typing import Tuple

import message_text_config as msg
import utils
from citizens.citizen import Citizen
from game import Game

from effects.effect import Effect, InputStatusCode


class FirstNightEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 5)

    def _activate_impl(self) -> bool:
        self.targets.append(self.game.passive_player)
        return True

    def _resolve_impl(self) -> bool:
        if self.activation_round == self.game.round_number:
            self.targets[0].disable_steal_action()
            return False

        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        return InputStatusCode.OK

    def _on_clear_impl(self) -> None:
        self.targets[0].enable_steal_action()
