import random
from typing import Dict, List, Optional

import message_text_config as msg
import user_interaction
from action_manager import ActionManager
from card import Card
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy
from effects.effect import Effect, EffectStatus
from game import Game


class GameController:
    def __init__(self, citizens_dict: Dict[str, Card],
                 user_names: List[str]) -> None:

        self.citizens_dict = citizens_dict
        self.user_names = user_names

        self.game: Game
        self.action_manager: ActionManager

    def start_game(self) -> None:
        self._prepare_game()

        while not self._check_win():
            self._proceed_game()

        self._finish_game()

    def _prepare_game(self) -> None:
        self.game = Game()
        self.action_manager = ActionManager()
        avilable_citizens: List[Citizen] = []

        self._create_citizens(avilable_citizens)
        self._create_players(avilable_citizens)
        self._set_order()
        self._create_spy(avilable_citizens)
        self._show_game_state()

    def _create_citizens(self, avilable_citizens) -> None:
        for name, card in self.citizens_dict.items():
            self.game.citizens.append(Citizen(name=name, citizen_card=card))

        avilable_citizens.extend(self.game.citizens)
        user_interaction.show_global_instant(msg.PreparePhase.GLOBAL_LOAD_GAME)

    def _create_players(self, avilable_citizens) -> None:
        # TODO: first player should not have oportunity to steal

        for user_name in self.user_names:
            random_index = random.randint(0, len(avilable_citizens) - 1)
            random_citizen = avilable_citizens.pop(random_index)

            player = Player(user_name=user_name,
                            name=random_citizen.name,
                            citizen_card=random_citizen.citizen_card)

            # Add player to players list
            self.game.players.append(player)

            # Replace citizen by player
            self.game.citizens.remove(random_citizen)
            self.game.citizens.append(player)

    def _set_order(self) -> None:
        random.shuffle(self.game.players)

        user_interaction.save_active(msg.PreparePhase.ACT_FIRST_TURN)
        user_interaction.save_active(
            msg.PreparePhase.ACT_PASS_YOUR_ROLE.format(
                self.game.players[0].name))
        user_interaction.save_passive(
            msg.PreparePhase.ACT_PASS_YOUR_ROLE.format(
                self.game.players[1].name))
        user_interaction.save_global(
            msg.PreparePhase.GLOBAL_FIRST_TURN.format(
                self.game.players[0].user_name))

    def _create_spy(self, avilable_citizens) -> None:
        random_index = random.randint(0, len(avilable_citizens) - 1)
        random_citizen = avilable_citizens.pop(random_index)

        # Save spy entity
        self.game.spy = Spy(name=random_citizen.name)

        # Replace citizen by spy
        self.game.citizens.remove(random_citizen)
        self.game.citizens.append(self.game.spy)

    def _show_game_state(self) -> None:
        user_interaction.save_global(msg.PreparePhase.GLOBAL_START_GAME)
        user_interaction.show_all()

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

        self._resolve_effects()
        self._clear_effects()
        user_interaction.show_all()

    def _clear_pre_actions(self) -> None:
        self.action_manager.clear_pre_actions()

    def _apply_pre_actions(self) -> None:
        for effect in self.action_manager.pre_actions:
            for target in effect.targets:
                target.effects.append(effect)

        self.action_manager.store_actions_history(self.game.round_number)

    def _show_night_state(self) -> None:
        night_number_str = msg.NightStatus.ACT_PASS_NIGHT_NUMBER.format(
            self.game.round_number)

        your_turn_str = msg.NightStatus.ACT_YOUR_TURN

        player_hp_str = msg.NightStatus.ACT_HP_COUNT.format(
            self.game.active_player.hp)

        staging_available = msg.NightStatus.ACT_STAGING_AVAILABLE \
            if self.game.active_player.is_staging_available \
            else msg.NightStatus.ACT_STAGING_UNAVAILABLE
        staging_active_str = msg.NightStatus.ACT_IS_STAGING.format(
            staging_available)

        player_card = self.game.active_player.citizen_card
        player_card_name = msg.NightStatus.ACT_NO_CARD if player_card is None else player_card.name
        player_card_str = msg.NightStatus.ACT_PERSONAL_CARD.format(
            player_card_name)

        stolen_card_names: List[str] = []
        for card in self.game.active_player.stolen_cards:
            stolen_card_names.append(card.name + "\n")
        stolen_cards_str = msg.NightStatus.ACT_STOLEN_CARDS.format(
            " ".join(stolen_card_names))

        citizen_names: List[str] = []
        for i, citizen in enumerate(self.game.citizens, start=1):
            prefix = ""
            if citizen is self.game.active_player:
                prefix = msg.NightStatus.ACT_YOU
            elif not citizen.is_alive:
                prefix = msg.NightStatus.ACT_DEAD

            citizen_option = msg.NightStatus.ACT_CITIZEN_LIST_OPTION.format(
                i, citizen.name, prefix)
            citizen_names.append(citizen_option + "\n")

        citizen_names_str = msg.NightStatus.ACT_CITY_STATUS.format(
            " ".join(citizen_names))

        user_interaction.save_global(night_number_str)

        user_interaction.save_active(your_turn_str)
        user_interaction.save_active("\n")
        user_interaction.save_active(player_hp_str)
        user_interaction.save_active(staging_active_str)
        user_interaction.save_active(player_card_str)
        user_interaction.save_active(stolen_cards_str)
        user_interaction.save_active(citizen_names_str)

        user_interaction.show_all()

    def _create_action(self) -> None:
        effect = self.game.active_player.create_action(self.game)
        effect.activate()
        self.action_manager.add_pre_action(effect)

    def _create_card_action(self) -> None:
        effect = self.game.active_player.create_card_action(self.game)
        effect.activate()
        self.action_manager.add_pre_action(effect)

    def _clear_effects(self) -> None:
        for citizen in self.game.citizens:
            for effect in citizen.effects:
                effect.on_clear()

            citizen.effects = [
                effect for effect in citizen.effects
                if effect.status != EffectStatus.FINISHED
            ]

    def _resolve_effects(self) -> None:
        for citizen in self.game.citizens:
            for effect in citizen.effects:
                effect.resolve()

    def _count_round(self) -> None:
        self.game.round_number += 1

    def _confirm_actions(self) -> bool:
        number = self._confirm_actions_msg()

        while True:
            if number == 1:
                return True
            elif number == 2:
                return False
            else:
                user_interaction.save_active(msg.Errors.CONFIRM_CHOICE)
                number = self._confirm_actions_msg()

    def _confirm_actions_msg(self) -> Optional[int]:
        user_interaction.save_active(
            msg.NightActionTarget.ACT_CHOISE_INFO.format(
                self.action_manager.pre_actions[0].name,
                self.action_manager.pre_actions[1].name))
        user_interaction.save_active("1. " +
                                     msg.NightActionTarget.ACT_CONFIRM_ACTION)
        user_interaction.save_active("2. " +
                                     msg.NightActionTarget.ACT_CANCEL_ACTION)
        user_interaction.show_all()

        number = user_interaction.read_number()
        return number

    def _check_win(self) -> bool:
        return (not self.game.players[0].is_alive) or \
            (not self.game.players[1].is_alive)

    def _finish_game(self) -> None:
        first_player_dead = not self.game.players[0].is_alive
        second_player_dead = not self.game.players[1].is_alive

        if first_player_dead and second_player_dead:
            user_interaction.show_global_instant(msg.FinishPhase.GLOBAL_DRAW)
        elif first_player_dead:
            user_interaction.show_global_instant(
                msg.FinishPhase.GLOBAL_PLAYER_WON.format(
                    self.game.players[1].name))
        else:
            user_interaction.show_global_instant(
                msg.FinishPhase.GLOBAL_PLAYER_WON.format(
                    self.game.players[0].name))
