from typing import Tuple

import message_text_config as msg
import utils
from citizens.citizen import Citizen
from murder_logging import logger

from effects.effect import Effect, InputStatusCode


class FirstNightEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)

        self.logger = logger.getChild(__name__)

    def _activate_impl(self) -> bool:
        self.targets.append(self.city.passive_player)

        self.logger.debug(" ")

        return True

    def _resolve_impl(self) -> bool:
        self.logger.debug(" ")
        if self.activation_round == self.city.round_number:
            self.targets[0].disable_steal_action()
            return False

        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        self.logger.debug(" ")
        return InputStatusCode.OK

    def _on_clear_impl(self) -> None:
        self.targets[0].enable_steal_action()
        self.logger.debug(" ")
