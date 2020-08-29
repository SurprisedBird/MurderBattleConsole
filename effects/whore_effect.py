import message_text_config as msg
import user_interaction
import utils
from citizens.citizen import Citizen
from citizens.player import Player
from effects.effect import Effect
from game import Game


class WhoreEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen) -> None:
        super().__init__(game, name, creator, 7)

    def _activate_impl(self) -> bool:
        target_number = utils.read_target_number(msg.CardTarget.ACT_BITCH,
                                                 self._validate)
        self.targets.append(self.game.citizens[target_number - 1])

        user_interaction.save_active(
            msg.EffectsActivated.ACT_BITCH.format(self.targets[0].name))

        return True

    def _resolve_impl(self) -> bool:
        if self.activation_round == self.game.round_number:
            user_interaction.save_global(msg.EffectsActivated.GLOBAL_BITCH)

            if type(self.targets[0]) is Player:
                self.targets[0].disable_steal_action()
                self.targets[0].disable_kill_action()
                self.targets[0].disable_staging_action()

            if self.targets[0] is self.game.passive_player:
                user_interaction.save_passive(msg.EffectsResolved.PASS_BITCH)

            return False

        return True

    def _validate(self, target_number: int) -> bool:
        return utils.validate_citizen_target_number(target_number,
                                                    self.game.citizens)

    def _on_clear_impl(self) -> None:
        if type(self.targets[0]) is Player:
            self.targets[0].enable_steal_action()
            self.targets[0].enable_kill_action()
            self.targets[0].enable_staging_action()
