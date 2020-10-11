import random
import string
from typing import List
from unittest import TestCase
from unittest.mock import patch

import message_text_config as config
import user_interaction
from card import Card
from citizens.citizen import Citizen
from effects.database_effect import DataBase
from effects.none_effect import NoneEffect
from game import Game
from game_controller import GameController


class DatabaseEffectTest(TestCase):
    def setUp(self):
        # seed makes similar citizens players data
        random.seed(408245472491)
        citizens_dict = {
            "Охотник": Card("Ловушка", NoneEffect),
            "Врач": Card("Антидот", NoneEffect),
            "Мальчик-хакер": Card("База данных", NoneEffect),
            "Актер": Card("Реквизит", NoneEffect),
            "Сутенер": Card("Клофелинщица", NoneEffect)
        }

        user_names = ["GvinP", "Runmaget"]

        self.gc = GameController(citizens_dict, user_names)

        self.gc._prepare_game()

        citizen = Citizen("Мальчик-хакер", "База данных", 3)
        self.db_effect = DataBase(self.gc.game, "База данных", citizen)

        self.gc._show_night_state()

    def test_activate_impl(self):
        with patch('builtins.input',
                   side_effect=["0", "0", "0", "1", "2", "3"]):
            self.db_effect._activate_impl()

    def test_validate(self):
        self.assertEqual(self.db_effect._validate([1, 3, 2]), True)
        self.assertEqual(self.db_effect._validate([3441, "3dsff", "dsfasd"]),
                         False)
        self.assertEqual(self.db_effect._validate([]), False)
        self.assertEqual(self.db_effect._validate([1, 3, 3]), False)
        self.assertEqual(self.db_effect._validate([1]), False)
        self.assertEqual(self.db_effect._validate([1, 3, 2, 4]), False)

    @patch('builtins.print')
    def test_resolve_impl(self, mock_print):

        self.db_effect.targets = [
            self.gc.game.citizens[0], self.gc.game.citizens[1]
        ]

        self.db_effect._resolve_impl()
        mock_print.assert_called_with(
            f"ACTIVE: {config.EffectsResolved.ACT_DATABASE_NO_SUSPECT}")

        self.db_effect.targets = [
            self.gc.game.citizens[0], self.gc.game.citizens[4]
        ]

        self.db_effect._resolve_impl()
        mock_print.assert_called_with(
            f"ACTIVE: {config.EffectsResolved.ACT_DATABASE_FIND_SPY}")

        self.db_effect.targets = [
            self.gc.game.citizens[3], self.gc.game.citizens[1]
        ]

        self.db_effect._resolve_impl()
        mock_print.assert_called_with(
            f"ACTIVE: {config.EffectsResolved.ACT_DATABASE_FIND_PLAYER}")

        self.db_effect.targets = [
            self.gc.game.citizens[3], self.gc.game.citizens[4]
        ]

        self.db_effect._resolve_impl()
        mock_print.assert_called_with(
            f"ACTIVE: {config.EffectsResolved.ACT_DATABASE_FIND_ALL}")
