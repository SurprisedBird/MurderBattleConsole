import random
import string
from typing import List
from unittest import TestCase
from unittest.mock import patch

import user_interaction
from citizens.citizen import Citizen
from effects.gossips_effect import GossipsEffect
from game import Game
from game_controller import GameController


class GossipsEffectTest(TestCase):
    def setUp(self):
        random.seed(408245472491)
        self.gc = GameController({
            "Охотник": "Ловушка",
            "Врач": "Антидот"
        }, ["Runmaget", "GvinP"])

        self.gc.start_game()
        self.gc.prepare_game()

        citizen = Citizen("Ночная продавщица", "Слухи", 3)
        self.gossips_effect = GossipsEffect(self.gc.game, "Слухи", citizen, 5)

    def test_activate_impl(self):
        input_invalid_value = str(random.randint(6, 8))
        input_valid_value = str(random.randint(1, 5))

        with patch('builtins.input',
                   side_effect=[input_invalid_value,
                                input_valid_value]) as mocked_input:
            with patch("builtins.print") as mocked_print:
                invalid = True
                self.gossips_effect._activate_impl()
                if invalid:
                    mocked_print.assert_called_with(
                        "ACTIVE: config.type_error")
                    invalid = False

    def test_resolve_impl(self):
        pass

    def test_validate(self):
        # TODO 5 it is a max value for action_history items count before the ActionHistory class is not implemented
        self.assertEqual(self.gossips_effect._validate(1, 5), True)
        self.assertEqual(
            self.gossips_effect._validate(len(self.gc.game.citizens), 1), True)

        self.assertEqual(
            self.gossips_effect._validate(
                random.randint(1, len(self.gc.game.citizens)),
                random.randint(1, 5)), True)

        self.assertEqual(
            self.gossips_effect._validate(random.randint(-1000, 0),
                                          random.randint(1, 5)), False)

        self.assertEqual(
            self.gossips_effect._validate(
                random.randint(1, len(self.gc.game.citizens)),
                random.randint(6, 1000)), False)
