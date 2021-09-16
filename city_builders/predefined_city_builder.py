from typing import Dict, List
from context import Context
from citizens.citizen import Citizen
from citizens.player import Player
from citizens.spy import Spy
from custom_logger import logger


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
        self._city = city
        for citizen in self.citizens_dict:

            if citizen["role"] == "C":
                self._city.citizens.append(
                    Citizen(context=self.context, name=citizen["name"], citizen_card=citizen["card"], hp=citizen["hp"]))
            elif citizen["role"] == "P1":
                self._city.players.append(Player(
                    context=self.context, user=self._users[0], name=citizen["name"], citizen_card=citizen["card"], hp=citizen["hp"]))
                self._city.citizens.append(self._city.players[0])
                self._city.players[0].stolen_cards = citizen["stolen_cards"]
            elif citizen["role"] == "P2":
                self._city.players.append(Player(
                    context=self.context, user=self._users[1], name=citizen["name"], citizen_card=citizen["card"], hp=citizen["hp"]))
                self._city.citizens.append(self._city.players[1])
                self._city.players[1].stolen_cards = citizen["stolen_cards"]
            elif citizen["role"] == "S":
                self._city.spy = Spy(
                    context=self.context, name=citizen["name"], hp=citizen["hp"])
                self._city.citizens.append(self._city.spy)
