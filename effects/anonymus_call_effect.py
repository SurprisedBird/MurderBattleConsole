from enum import Enum, auto

import message_text_config as msg
import utils
from citizens.citizen import Citizen


from effects.effect import Effect, InputStatusCode


class AnonymusCallEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: Citizen) -> None:
        super().__init__(context, name, creator)
        self.detected_name: str

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(
            self.context, msg.AnonymousCallMessages.ACTIVATION_CHOOSE_TARGET,
            self._validate)

        self.targets.append(self.city.citizens[target_number - 1])

        self.user_interaction.save_active(
            msg.AnonymousCallMessages.ACTIVATION_SUCCESS.format(
                self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        self.detected_name = self.targets[0].name
        if self.theatre_target() is not None:
            self.targets[0] = self.theatre_target()

        role = type(self.targets[0]).__name__
        if role == "Player":
            self.user_interaction.show_global_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_PLAYER.format(
                    self.detected_name))
            if self.targets[0].name is self.detected_name:
                self.targets[0].hp -= 1
                utils.save_message_for_player(
                    self.context, self.targets[0], msg.AnonymousCallMessages.RESOLVE_ENEMY_LOST_HP)
        elif role == "Spy":
            self.targets[0].hp -= 1
            self.user_interaction.show_global_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_SPY.format(
                    self.detected_name))
        else:
            self.user_interaction.show_global_instant(
                msg.AnonymousCallMessages.RESOLVE_ANONYMOUSCALL_NO_SUSPECT.
                format(self.detected_name))

        self.logger.info(
            f'Detected name {self.detected_name}, Is theatre target {self.theatre_target() is not None}, role {role}'
        )

        return True

    def theatre_target(self) -> 'Citizen':
        for effect in self.city.effects:
            if type(effect).__name__ is 'TheatreEffect':
                self.logger.info(
                    f"Player is {effect.creator.name}, player mask is {effect.mask.name}"
                )
                if self.targets[0] is effect.creator:
                    return effect.mask
                elif self.targets[0] is effect.mask:
                    return effect.creator
        return None

    def _validate(self, target_number: int) -> InputStatusCode:
        return utils.validate_citizen_target_number(
            target_number,
            self.city.citizens,
            self_as_target_allowed=True,
            creator=self.creator)

    def _on_clear_impl(self) -> None:
        pass
