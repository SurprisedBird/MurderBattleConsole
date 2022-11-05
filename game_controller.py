import random
from typing import Dict, List, Optional

import message_text_config as msg
from action_manager import ActionManager
from card import Card
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy
from city import City
from city_builders.predefined_city_builder import CityBuilder
from context import Context
from custom_logger import logger
from effects.alarm_effect import AlarmEffect
from effects.trap_effect import TrapEffect
from effects.effect import Effect, EffectStatus
from effects.first_night_effect import FirstNightEffect
from effects.kill_effect import KillEffect
from effects.none_effect import NoneEffect
from effects.spy_effect import SpyEffect
from effects.staging_effect import StagingEffect
from effects.steal_effect import StealEffect
from user_interactions.user_interaction_telegram import UserInteraction


class GameController(Context):
    def __init__(self, cards, citizens_dict: Dict[str, Card],
                 users: List[str]) -> None:

        self.citizens_dict = citizens_dict
        self.cards = cards
        self._users = users
        self._city = City()
        self._user_interaction = UserInteraction(self)
        self._city_builder = CityBuilder(self, self.citizens_dict, self._users)
        self._action_manager = ActionManager()
        self.logger = logger.getChild(__name__)
        self.logger.disabled = False

    def start_game(self) -> None:
        self._prepare_game()

        while not self._check_win():
            self._proceed_game()

        self._finish_game()

# =================================================================
# Prepare game phase
# =================================================================

    def _prepare_game(self) -> None:
        avilable_citizens: List[Citizen] = []

        self._set_priorities()
        self._city_builder.build_city(self._city)
        self._pre_proceed_game()
        self._show_game_state()

    def _create_citizens(self, avilable_citizens) -> None:
        for citizen in self.citizens_dict:
            self._city.citizens.append(
                Citizen(context=self, name=citizen["name"], citizen_card=citizen["card"]))

        avilable_citizens.extend(self._city.citizens)
        self._user_interaction.show_global_instant(
            msg.PreparePhase.GLOBAL_LOAD_GAME)

        self.logger.debug(" ")

    def _create_players(self, avilable_citizens) -> None:
        # TODO: first player should not have oportunity to steal

        for user in self._users:
            random_index = random.randint(0, len(avilable_citizens) - 1)
            random_citizen = avilable_citizens.pop(random_index)

            player = Player(context=self,
                            user=user,
                            name=random_citizen.name,
                            citizen_card=random_citizen.citizen_card)

            self.logger.info(
                f"user_name = {player.user.name}, citizen_name = {player.name}"
            )

            # Add player to players list
            self._city.players.append(player)

            # Replace citizen by player
            replacing_index = self._city.citizens.index(random_citizen)
            self._city.citizens.remove(random_citizen)
            self._city.citizens.insert(replacing_index, player)

    def _set_priorities(self) -> None:
        all_effects = []

        standard_effects = [
                NoneEffect,
                StagingEffect,
                KillEffect,
                StealEffect,
                SpyEffect,
                FirstNightEffect,
                TrapEffect
                ]
        
        all_effects.extend(standard_effects)

        for citizen in self.citizens_dict:
            all_effects.append(citizen["card"].effect)

        for i in range(0, len(all_effects)):
                all_effects[i].__priority__ = i

    def _set_order(self) -> None:
        random.shuffle(self._city.players)

        self._user_interaction.save_passive(msg.PreparePhase.ACT_FIRST_TURN)
        self._user_interaction.save_passive(
            msg.PreparePhase.ACT_PASS_YOUR_ROLE.format(
                self._city.players[0].name))
        self._user_interaction.save_active(
            msg.PreparePhase.ACT_PASS_YOUR_ROLE.format(
                self._city.players[1].name))
        self._user_interaction.save_global(
            msg.PreparePhase.GLOBAL_FIRST_TURN.format(
                self._city.players[0].user.name))

        self.logger.info(
            f"first player = {self._city.players[0].name}, second player = {self._city.players[1].name}"
        )

    def _create_spy(self, avilable_citizens) -> None:
        random_index = random.randint(0, len(avilable_citizens) - 1)
        random_citizen = avilable_citizens.pop(random_index)

        # Save spy entity
        self._city.spy = Spy(context=self, name=random_citizen.name)

        # Replace citizen by spy
        replacing_index = self._city.citizens.index(random_citizen)
        self._city.citizens.remove(random_citizen)
        self._city.citizens.insert(replacing_index, self._city.spy)

        self.logger.info(f'spy = {self._city.spy.name}')

    def _pre_proceed_game(self) -> None:
        self._create_effect(SpyEffect, msg.EffectsNames.SPY_EFFECT_NAME,
                            self._city.spy)
        self._create_effect(FirstNightEffect,
                            msg.EffectsNames.FIRST_NIGHT_EFFECT,
                            self._city.passive_player)

        self._resolve_effects()
        self._clear_effects()

    def _create_effect(self, effect_type, effect_name, citizen) -> None:
        effect = effect_type(self, effect_name, citizen)
        effect.activate_by_target(citizen)

        self.logger.info(
            f'effect name = {effect_type.__name__}, effect creator = {effect.creator.name}'
        )

    def _show_game_state(self) -> None:
        self._user_interaction.save_global(msg.PreparePhase.GLOBAL_START_GAME)
        self._user_interaction.show_all()

        self.logger.debug(" ")

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
        self._city.active_player.remove_used_card()
        self._create_note()

        self._resolve_effects()
        self._clear_effects()
        self._user_interaction.show_all()

    def _clear_pre_actions(self) -> None:
        self._action_manager.clear_pre_actions()

        self.logger.info(self._action_manager.pre_actions)

    def _apply_pre_actions(self) -> None:
        updated_targets = []
        for effect in self._action_manager.pre_actions:
            for target in effect.targets:
                target.effects.append(effect)
                updated_targets.append(target)

        # Sort all effects by priority for each updated target
        for target in updated_targets:
            target.effects.sort(reverse=True)

        self._action_manager.store_actions_history(self._city.round_number)

        self.logger.info(self._action_manager.pre_actions)

    def _show_night_state(self) -> None:
        night_number_str = msg.NightState.NIGHT_NUMBER.format(
            self._city.round_number)

        your_turn_str = msg.NightState.YOUR_TURN

        player_hp_str = msg.NightState.HP_COUNT.format(
            self._city.active_player.hp)

        staging_available = msg.NightState.STAGING_UNAVAILABLE \
            if self._city.active_player.staging_was_used \
            else msg.NightState.STAGING_AVAILABLE
        staging_active_str = msg.NightState.IS_STAGING.format(
            staging_available)

        player_card = self._city.active_player.citizen_card
        player_card_name = msg.NightState.NO_CARD if player_card is None else player_card.name
        player_card_str = msg.NightState.PERSONAL_CARD.format(player_card_name)

        stolen_card_names: List[str] = []
        for card in self._city.active_player.stolen_cards:
            stolen_card_names.append(card.name + "\n")
        stolen_cards_str = msg.NightState.STOLEN_CARDS.format(
            " ".join(stolen_card_names))

        self._user_interaction.save_global(night_number_str)

        self._user_interaction.save_active(your_turn_str)
        self._user_interaction.save_active("\n")
        self._user_interaction.save_active(player_hp_str)
        self._user_interaction.save_active(staging_active_str)
        self._user_interaction.save_active(player_card_str)
        self._user_interaction.save_active(stolen_cards_str)

        self._user_interaction.show_all()

        citizen_names: List[str] = []
        for i, citizen in enumerate(self._city.citizens, start=1):
            prefix = ""
            if citizen is self._city.active_player:
                prefix = msg.NightState.YOU
            elif not citizen.is_alive:
                prefix = msg.NightState.DEAD

            citizen_option = msg.NightState.CITIZEN_LIST_OPTION.format(
                i, citizen.name, prefix)
            citizen_names.append(citizen_option + "\n")

        citizen_names_str = msg.NightState.CITY_STATUS.format(
            " ".join(citizen_names))

        self._user_interaction.save_active(citizen_names_str)

        self._user_interaction.show_all()

        self.logger.debug(" ")

    def _create_action(self) -> None:
        effect = self._city.active_player.create_action()
        effect.activate()
        self._action_manager.add_pre_action(effect)
            
    def _create_card_action(self) -> None:
        effect = self._city.active_player.create_card_action()
        effect.activate()
        self._action_manager.add_pre_action(effect)
        self.logger.info(f"{effect.name}, {effect.status.name}")
        
    def _create_note(self) -> None:
        self._city.active_player.create_note()

    def _clear_effects(self) -> None:
        for citizen in self._city.citizens:
            for effect in citizen.effects:
                effect.on_clear()

            citizen.effects = [
                effect for effect in citizen.effects
                if effect.status != EffectStatus.FINISHED
            ]
        self.logger.debug(" ")

    def _resolve_effects(self) -> None:
        for effect in self._city.effects:
            effect.resolve()
            self.logger.info(f"{effect.name}, {effect.status.name}")

        for citizen in self._city.citizens:
            for effect in citizen.effects:
                effect.resolve()

        if self.user_interaction.is_global_empty():
            self.user_interaction.save_global(
                msg.DayGeneralMessages.GLOBAL_CALM_CITIZEN)
            
        if self._city.active_player.active_note != "":
            self.user_interaction.save_global("\nУбийца оставил записку: \n" + "\"" + self.city.active_player.active_note + "\"")
            self.city.active_player.active_note = ""

    def _count_round(self) -> None:
        self._city.round_number += 1

        self.logger.debug(" ")

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

        self.logger.debug(" ")

    def _confirm_actions_msg(self) -> Optional[int]:
        
        #self._user_interaction.save_active(
        #    msg.NightActionTarget.ACT_CHOISE_INFO.format(
        #        self._action_manager.pre_actions[0].name,
        #        self._action_manager.pre_actions[1].name))
        #self._user_interaction.save_active(
        #    "1. " + msg.NightActionTarget.ACT_CONFIRM_ACTION)
        #self._user_interaction.save_active(
        #    "2. " + msg.NightActionTarget.ACT_CANCEL_ACTION)
        #self._user_interaction.show_all()
        
        first_action_effect = self._action_manager.pre_actions[0]
        first_action = first_action_effect.name

        first_targets = ""
        for target in first_action_effect.targets:
            first_targets += target.name + " "

        second_action_effect = self._action_manager.pre_actions[1]
        second_action = second_action_effect.name

        second_targets = ""
        for target in second_action_effect.targets:
            second_targets += target.name + " "
        
        full_confirm_text = msg.NightActionTarget.ACT_CHOISE_INFO.format(first_action,
                                                       first_targets,
                                                       second_action,
                                                       second_targets) + "\n"
  
        
        self._user_interaction.show_active_instant(full_confirm_text)
        
        full_confirm_text = "Перед подтверждением введите текст в чат, чтобы оставить записку\n"
        full_confirm_text += "1. " + msg.NightActionTarget.ACT_CONFIRM_ACTION + "\n"
        full_confirm_text += "2. " + msg.NightActionTarget.ACT_CANCEL_ACTION + "\n"
        self._user_interaction.save_active(full_confirm_text)
        #self._user_interaction.show_all()

        number = self._user_interaction.read_number()

        self.logger.debug("")

        return number

# =================================================================
# Finish game phase
# =================================================================

    def _check_win(self) -> bool:
        self.logger.debug("")
        return (not self._city.players[0].is_alive) or \
            (not self._city.players[1].is_alive)

    def _finish_game(self) -> None:
        first_player_dead = not self._city.players[0].is_alive
        second_player_dead = not self._city.players[1].is_alive

        if first_player_dead and second_player_dead:
            self._user_interaction.show_global_instant(
                msg.FinishPhase.GLOBAL_DRAW)
        elif first_player_dead:
            self._user_interaction.show_global_instant(
                msg.FinishPhase.GLOBAL_PLAYER_WON.format(
                    self._city.players[1].user.name))
        else:
            self._user_interaction.show_global_instant(
                msg.FinishPhase.GLOBAL_PLAYER_WON.format(
                    self._city.players[0].user.name))

        self.logger.info(
            f"{self._city.players[0].is_alive}, second player is alive = {self._city.players[1].is_alive}"
        )


# =================================================================
# Context implementation
# =================================================================

    @property
    def users(self):
        return self._users

    @property
    def user_interaction(self):
        return self._user_interaction

    @property
    def city(self):
        return self._city

    @property
    def action_manager(self):
        return self._action_manager
