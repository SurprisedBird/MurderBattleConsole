import user_interaction
import utils
from citizens.citizen import Citizen
from citizens.spy import Spy
from effects.effect import Effect, EffectStatus
from game import Game


class GossipsEffect(Effect):
    def __init__(self, game: Game, name: str, creator: Citizen,
                 round_story_number: int) -> None:
        Effect.__init__(self, game, name, creator, 0)

    def _activate_impl(self) -> bool:
        round_number = user_interaction.read_index(
            "Выберите ночь, информация о которой будет предоставлена...")

        # TODO target_number should be passive_player index in citizens list
        target_number = 1
        while (not self._validate(target_number, round_number)):
            user_interaction.show_active_instant("config.type_error")
            round_number = user_interaction.read_index(
                "Выберите ночь, информация о которой будет предоставлена...")

        self.round_story_number = round_number
        self._targets.append(self._game.citizens[target_number - 1])

        return True

    def _resolve_impl(self) -> bool:
        if self._status is EffectStatus.ACTIVATED:

            # TODO actions shoud be get from the relevant action_history item effects

            round_actions_text = "Действие: first_action_item_effect.name\nЦель: first_action_item_effect.target\nКарта: second_action_item_effect.name\nЦель: second_action_item_effect.target"
            user_interaction.show_active_instant(round_actions_text)

        if self._status is EffectStatus.FINISHED:
            pass

        return True

    def _validate(self, target_number: int, round_number: int):
        is_number = utils.validate_citizen_target_number(
            target_number, self._game.citizens)

        # TODO rounds_count should be equal to len(action_history)
        rounds_count = 5
        is_round_in_range = round_number > 0 and round_number <= rounds_count
        return is_number and is_round_in_range

    def on_clear(self) -> None:
        pass
