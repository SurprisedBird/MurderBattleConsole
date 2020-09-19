from enum import Enum, auto
from typing import Tuple

import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from effects.effect import Effect
from game import Game


class ErrorType(Enum):
    INVALID_TARGET = msg.Errors.TARGET
    SELF_AS_TARGET = msg.Errors.SELF_AS_TARGET


class StagingEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, creator, 3)

    def _activate_impl(self) -> bool:
        target_number = self._read_target_number()
        self.targets.append(self.game.citizens[target_number - 1])

        user_interaction.save_active(
            msg.NightActionTarget.ACT_STAGING_ACTIVATED.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:

        self.creator.disable_staging_action(disable_forever=True)

        # Hit the target
        self.targets[0].hp -= 1
        if not self.targets[0].is_alive:
            # Move personal card to stolen cards
            if self.creator.citizen_card is not None:
                self.creator.stolen_cards.append(self.creator.citizen_card)
                self.creator.citizen_card = None

            # Get personal card of target citizen
            if self.targets[0].citizen_card is not None:
                self.creator.citizen_card = self.targets[0].citizen_card
                self.targets[0].citizen_card = None

            citizens = self.game.citizens
            target_index = citizens.index(self.targets[0])
            player_index = citizens.index(self.creator)

            # Swap citizens
            citizens[target_index], citizens[player_index] = citizens[
                player_index], citizens[target_index]
            # Swap names of citizens back
            citizens[target_index].name, citizens[
                player_index].name = citizens[player_index].name, citizens[
                    target_index].name

            # Disable all effects for both citizens
            for effect in citizens[target_index].effects:
                effect.deactivate()
            for effect in citizens[player_index].effects:
                effect.deactivate()

            user_interaction.save_active(
                msg.NightResult.ACT_STAGING_SUCCESSFULL.format(
                    self.creator.name))

        # Not using isinstance(self.targets[0], Player)
        # because of cycle import problem
        elif type(self.targets[0]).__name__ == "Player":
            user_interaction.save_active(
                msg.NightResult.ACT_STAGING_UNSUCCESSFUL)
            user_interaction.save_passive(msg.DayGeneral.ACT_PASS_LOST_HP)
        else:
            user_interaction.save_active(
                msg.NightResult.ACT_STAGING_UNSUCCESSFUL)

        return True

    def _validate(self, target_number: int) -> Tuple[bool, ErrorType]:
        is_valid = utils.validate_citizen_target_number(
            target_number, self.game.citizens)

        # Staging could not be set on yourself
        is_self_as_target = \
            (self.game.citizens[target_number - 1] is self.creator) \
            if is_valid else False

        if is_self_as_target:
            return (False, ErrorType.SELF_AS_TARGET)
        elif not is_valid:
            return (False, ErrorType.INVALID_TARGET)

        return (True, None)

    def _on_clear_impl(self) -> None:
        pass

    def _read_target_number(self) -> int:
        message = msg.NightActionTarget.ACT_STAGING
        target_number = user_interaction.read_number(message)

        is_valid, error_code = self._validate(target_number)
        while not is_valid:
            user_interaction.show_active_instant(error_code.value)
            is_valid, error_code = user_interaction.read_number(message)

        return target_number
