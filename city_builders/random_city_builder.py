from typing import Dict, List
from context import Context
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy
from custom_logger import logger
import message_text_config as msg
import random


class CityBuilder():
    def __init__(self, context, citizens_dict: Dict[str, List],
                 users: List[str]) -> None:

        self.context = context
        self.citizens_dict = citizens_dict
        self._users = users
        self._user_interaction = context.user_interaction
        self.logger = logger.getChild(__name__)
        self.logger.disabled = False

    def build_city(self, city) -> None:
        avilable_citizens: List[Citizen] = []
        self._city = city

        self._create_citizens(avilable_citizens)
        self._create_players(avilable_citizens)
        self._create_spy(avilable_citizens)
        self._set_order()

    def _create_citizens(self, avilable_citizens) -> None:
        for citizen in self.citizens_dict:
            self._city.citizens.append(
                Citizen(context=self.context, name=citizen["name"], citizen_card=citizen["card"]))

        avilable_citizens.extend(self._city.citizens)
        self._user_interaction.show_global_instant(
            msg.PreparePhase.GLOBAL_LOAD_GAME)

        self.logger.debug(" ")

    def _create_players(self, avilable_citizens) -> None:
        # TODO: first player should not have oportunity to steal

        for user in self._users:
            random_index = random.randint(0, len(avilable_citizens) - 1)
            random_citizen = avilable_citizens.pop(random_index)

            player = Player(context=self.context,
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
        self._city.spy = Spy(context=self.context, name=random_citizen.name)

        # Replace citizen by spy
        replacing_index = self._city.citizens.index(random_citizen)
        self._city.citizens.remove(random_citizen)
        self._city.citizens.insert(replacing_index, self._city.spy)

        self.logger.info(f'spy = {self._city.spy.name}')
