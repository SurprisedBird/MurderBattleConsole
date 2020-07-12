from unittest import TestCase

from game_controller import GameController


class GameControllerTest(TestCase):
    def setUp(self):
        self.gc = GameController()
        self.gc.start_game()

    def test_start_game(self):
        self.gc.start_game()
        self.assertIsNotNone(self.gc.game)

    def test_set_order(self):

        self.gc.set_order()

        users_list = [self.gc.first_user, self.gc.second_user]
        self.assertCountEqual(users_list, self.gc.user_names)

    def test_create_citizens(self):
        # Add citizens initial data with citizen name and card name
        # Add citizens into the game citizens list and available citizens list
        # Assert the citizens initial data and citizens data in both lists
        # Expected result: List data should be the similar

        citizens_list = ["Охотник", "Врач", "Сутенер"]

        self.gc.create_citizens()

        names = []
        available_names = []

        for citizen in self.gc.game.citizens:
            names.append(citizen.name)

        for citizen in self.gc.available_citizens:
            available_names.append(citizen.name)

        self.assertEqual(citizens_list, names)
        self.assertEqual(citizens_list, available_names)

    def test_create_player(self):
        names = []
        available_names = []
        self.gc.create_citizens()

        for citizen in self.gc.game.citizens:

            names.append(citizen.name)

        for citizen in self.gc.available_citizens:
            available_names.append(citizen.name)

        self.gc.create_player()
        print(dir(self.gc.game.players[0]))

        self.assertIsNotNone(self.gc.game.players)
        self.assertNotEqual(self.gc.game.players[0].name,
                            self.gc.game.players[1].name)

    def test_create_spy(self):
        names = []
        available_names = []
        self.gc.create_citizens()

        for citizen in self.gc.game.citizens:

            names.append(citizen.name)

        for citizen in self.gc.available_citizens:
            available_names.append(citizen.name)

        self.gc.create_player()

        self.gc.create_spy()

        self.assertIsNotNone(self.gc.game.spy)
        self.assertNotEqual(self.gc.game.spy.name,
                            self.gc.game.players[0].name)
        self.assertNotEqual(self.gc.game.spy.name,
                            self.gc.game.players[1].name)

    def test_prepare_game(self):
        self.gc.prepare_game()
