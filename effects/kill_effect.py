import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy
from game import Game
from message_text_config import Errors

from effects.effect import Effect
""" class ErrorsEnum(Enum):
    INVALID_TURGET = Errors.TARGET
    NOT_THREE_TARGET = Errors.DATA_BASE_TARGETS
    SAME_TARGETS = Errors.DATA_BASE_SAME_TARGETS
 """


class KillEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, game.active_player, 0)

    def _activate_impl(self) -> bool:
        target_number = user_interaction.read_number(
            msg.NightActionTarget.ACT_KILL)

        while (not self._validate(target_number)):
            user_interaction.show_active_instant(self._status.value)
            target_number = user_interaction.read_number(
                msg.NightActionTarget.ACT_KILL)

        self._targets.append(self._game.citizens[target_number - 1])
        return True

    def _resolve_impl(self) -> bool:
        self._targets[0].hp -= 1

        if self._targets[0].is_alive:
            user_interaction.save_global(
                msg.DayGeneral.GLOBAL_KILL_PLAYER.format(
                    self._targets[0].name, self._targets[0].name))
            user_interaction.save_passive(msg.DayGeneral.ACT_PASS_LOST_HP)

        elif type(self._targets[0]).__name__ == "Spy":
            self._creator.hp -= 1
            user_interaction.save_global(
                msg.DayGeneral.GLOBAL_KILL_SPY.format(self._targets[0].name,
                                                      self._targets[0].name))
            user_interaction.save_active(msg.DayGeneral.ACT_PASS_LOST_HP)

        else:
            user_interaction.save_global(
                msg.DayGeneral.GLOBAL_KILL_CITIZEN.format(
                    self._targets[0].name))
            citizen_card = self._targets[0].citizen_card
            if citizen_card is not None:
                self._creator.stolen_cards.append(citizen_card)
                self._targets[0].citizen_card = None
                user_interaction.save_active(
                    msg.NightResult.ACT_STEAL_SUCCESSFULL.format(
                        citizen_card.name))
            else:
                user_interaction.save_active(
                    msg.NightResult.ACT_STEAL_UNSUCCESSFULL.format(
                        self._targets[0].name))

        return True

    def _validate(self, target_number: int) -> bool:
        is_in_range_and_alive = utils.validate_citizen_target_number(
            target_number, self._game.citizens)

        if not is_in_range_and_alive:
            return False

        is_not_active = self._game.citizens[target_number -
                                            1] != self._game.active_player

        if not is_not_active:
            # TODO Add message text
            return False

        return True

    def _on_clear_impl(self) -> None:
        pass
