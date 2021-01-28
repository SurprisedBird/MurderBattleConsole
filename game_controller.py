import random
from typing import Dict, List, Optional

import message_text_config as msg
from action_manager import ActionManager
from card import Card
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy
from context import Context
from effects.effect import Effect, EffectStatus
from game import Game
from user_interactions.user_interaction import UserInteraction


class GameController(Context):
    def __init__(self, citizens_dict: Dict[str, Card],
                 user_names: List[str]) -> None:

        self.citizens_dict = citizens_dict
        self.user_names = user_names
        self._game = Game()
        self._user_interaction = UserInteraction(self)

    def start_game(self) -> None:
        self._prepare_game()

        while not self._check_win():
            self._proceed_game()

        self._finish_game()

# =================================================================
# Prepare game phase
# =================================================================

    def _prepare_game(self) -> None:
        self._game.action_manager = ActionManager()
        avilable_citizens: List[Citizen] = []

        self._create_citizens(avilable_citizens)
        self._create_players(avilable_citizens)
        self._set_order()
        self._create_spy(avilable_citizens)
        self._show_game_state()

    def _create_citizens(self, avilable_citizens) -> None:
        for name, card in self.citizens_dict.items():
            self._game.citizens.append(
                Citizen(context=self, name=name, citizen_card=card))

        avilable_citizens.extend(self._game.citizens)
        self._user_interaction.show_global_instant(
            msg.PreparePhase.GLOBAL_LOAD_GAME)

    def _create_players(self, avilable_citizens) -> None:
        # TODO: first player should not have oportunity to steal

        for user_name in self.user_names:
            random_index = random.randint(0, len(avilable_citizens) - 1)
            random_citizen = avilable_citizens.pop(random_index)

            player = Player(context=self,
                            user_name=user_name,
                            name=random_citizen.name,
                            citizen_card=random_citizen.citizen_card)

            # Add player to players list
            self._game.players.append(player)

            # Replace citizen by player
            replacing_index = self._game.citizens.index(random_citizen)
            self._game.citizens.remove(random_citizen)
            self._game.citizens.insert(replacing_index, player)

    def _set_order(self) -> None:
        random.shuffle(self._game.players)

        self._user_interaction.save_active(msg.PreparePhase.ACT_FIRST_TURN)
        self._user_interaction.save_active(
            msg.PreparePhase.ACT_PASS_YOUR_ROLE.format(
                self._game.players[0].name))
        self._user_interaction.save_passive(
            msg.PreparePhase.ACT_PASS_YOUR_ROLE.format(
                self._game.players[1].name))
        self._user_interaction.save_global(
            msg.PreparePhase.GLOBAL_FIRST_TURN.format(
                self._game.players[0].user_name))

    def _create_spy(self, avilable_citizens) -> None:
        random_index = random.randint(0, len(avilable_citizens) - 1)
        random_citizen = avilable_citizens.pop(random_index)

        # Save spy entity
        self._game.spy = Spy(context=self, name=random_citizen.name)

        # Replace citizen by spy
        replacing_index = self._game.citizens.index(random_citizen)
        self._game.citizens.remove(random_citizen)
        self._game.citizens.insert(replacing_index, self._game.spy)

    def _show_game_state(self) -> None:
        self._user_interaction.save_global(msg.PreparePhase.GLOBAL_START_GAME)
        self._user_interaction.show_all()

# =================================================================
# Proceed game phase
# =================================================================

    def _proceed_game(self) -> None:
        self._count_round()
        self._show_night_state()

        action_confirmed = False
        while not action_confirmed:
            self._clear_pre_actions()
            self._create_action()
            self._create_card_action()

            action_confirmed = self._confirm_actions()

        self._apply_pre_actions()
        self._disable_used_player_actions()

        self._resolve_effects()
        self._clear_effects()
        self._user_interaction.show_all()

    def _clear_pre_actions(self) -> None:
        self._game.action_manager.clear_pre_actions()

    def _apply_pre_actions(self) -> None:
        updated_targets = []
        for effect in self._game.action_manager.pre_actions:
            for target in effect.targets:
                target.effects.append(effect)
                updated_targets.append(target)

        # Sort all effects by priority for each updated target
        for target in updated_targets:
            target.effects.sort(reverse=True)

        self._game.action_manager.store_actions_history(
            self._game.round_number)

    def _disable_used_player_actions(self):
        self._game.active_player.remove_used_card()
        self._game.active_player.disable_used_staging()

    def _show_night_state(self) -> None:
        night_number_str = msg.NightState.NIGHT_NUMBER.format(
            self._game.round_number)

        your_turn_str = msg.NightState.YOUR_TURN

        player_hp_str = msg.NightState.HP_COUNT.format(
            self._game.active_player.hp)

        staging_available = msg.NightState.STAGING_UNAVAILABLE \
            if self._game.active_player.staging_was_used \
            else msg.NightState.STAGING_AVAILABLE
        staging_active_str = msg.NightState.IS_STAGING.format(
            staging_available)

        player_card = self._game.active_player.citizen_card
        player_card_name = msg.NightState.NO_CARD if player_card is None else player_card.name
        player_card_str = msg.NightState.PERSONAL_CARD.format(player_card_name)

        stolen_card_names: List[str] = []
        for card in self._game.active_player.stolen_cards:
            stolen_card_names.append(card.name + "\n")
        stolen_cards_str = msg.NightState.STOLEN_CARDS.format(
            " ".join(stolen_card_names))

        citizen_names: List[str] = []
        for i, citizen in enumerate(self._game.citizens, start=1):
            prefix = ""
            if citizen is self._game.active_player:
                prefix = msg.NightState.YOU
            elif not citizen.is_alive:
                prefix = msg.NightState.DEAD

            citizen_option = msg.NightState.CITIZEN_LIST_OPTION.format(
                i, citizen.name, prefix)
            citizen_names.append(citizen_option + "\n")

        citizen_names_str = msg.NightState.CITY_STATUS.format(
            " ".join(citizen_names))

        self._user_interaction.save_global(night_number_str)

        self._user_interaction.save_active(your_turn_str)
        self._user_interaction.save_active("\n")
        self._user_interaction.save_active(player_hp_str)
        self._user_interaction.save_active(staging_active_str)
        self._user_interaction.save_active(player_card_str)
        self._user_interaction.save_active(stolen_cards_str)
        self._user_interaction.save_active(citizen_names_str)

        self._user_interaction.show_all()

    def _create_action(self) -> None:
        effect = self._game.active_player.create_action()
        effect.activate()
        self._game.action_manager.add_pre_action(effect)

    def _create_card_action(self) -> None:
        effect = self._game.active_player.create_card_action()
        effect.activate()
        self._game.action_manager.add_pre_action(effect)

    def _clear_effects(self) -> None:
        for citizen in self._game.citizens:
            for effect in citizen.effects:
                effect.on_clear()

            citizen.effects = [
                effect for effect in citizen.effects
                if effect.status != EffectStatus.FINISHED
            ]

    def _resolve_effects(self) -> None:
        for citizen in self._game.citizens:
            for effect in citizen.effects:
                effect.resolve()

    def _count_round(self) -> None:
        self._game.round_number += 1

    def _confirm_actions(self) -> bool:
        number = self._confirm_actions_msg()

        while True:
            if number == 1:
                return True
            elif number == 2:
                return False
            else:
                self._user_interaction.save_active(
                    msg.CommonMessages.ERROR_INVALID_OPTION)
                number = self._confirm_actions_msg()

    def _confirm_actions_msg(self) -> Optional[int]:
        self._user_interaction.save_active(
            msg.NightActionTarget.ACT_CHOISE_INFO.format(
                self._game.action_manager.pre_actions[0].name,
                self._game.action_manager.pre_actions[1].name))
        self._user_interaction.save_active(
            "1. " + msg.NightActionTarget.ACT_CONFIRM_ACTION)
        self._user_interaction.save_active(
            "2. " + msg.NightActionTarget.ACT_CANCEL_ACTION)
        self._user_interaction.show_all()

        number = self._user_interaction.read_number()
        return number

# =================================================================
# Finish game phase
# =================================================================

    def _check_win(self) -> bool:
        return (not self._game.players[0].is_alive) or \
            (not self._game.players[1].is_alive)

    def _finish_game(self) -> None:
        first_player_dead = not self._game.players[0].is_alive
        second_player_dead = not self._game.players[1].is_alive

        if first_player_dead and second_player_dead:
            self._user_interaction.show_global_instant(
                msg.FinishPhase.GLOBAL_DRAW)
        elif first_player_dead:
            self._user_interaction.show_global_instant(
                msg.FinishPhase.GLOBAL_PLAYER_WON.format(
                    self._game.players[1].name))
        else:
            self._user_interaction.show_global_instant(
                msg.FinishPhase.GLOBAL_PLAYER_WON.format(
                    self._game.players[0].name))


# =================================================================
# Context implementation
# =================================================================

    @property
    def user_interaction(self):
        return self._user_interaction

    @property
    def game(self):
        return self._game

    @property
    def action_manager(self):
        return self._game.action_manager
