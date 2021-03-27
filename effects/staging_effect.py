from enum import Enum, auto

import message_text_config as msg
import utils
from citizens.citizen import Citizen

from effects.effect import Effect, InputStatusCode


class StagingEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator, 1)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.StagingMassages.ACTIVATION_CHOOSE_TARGET,
            self._validate)
        self.targets.append(self.city.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.StagingMassages.ACTIVATION_SUCCESS.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
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

            citizens = self.city.citizens
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

            self.user_interaction.save_active(
                msg.StagingMassages.RESOLVE_SUCCESS.format(self.creator.name))

        elif utils.is_player(self.targets[0]):
            self.user_interaction.save_active(
                msg.StagingMassages.RESOLVE_FAILED)
            self.user_interaction.save_passive(
                msg.StagingMassages.RESOLVE_ENEMY_LOST_HP)
        else:
            self.user_interaction.save_active(
                msg.StagingMassages.RESOLVE_FAILED)

        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(
            target_number,
            self.city.citizens,
            self_as_target_allowed=False,
            creator=self.creator)

    def _on_clear_impl(self) -> None:
        pass
