from unittest import TestCase
import user_interaction
from unittest.mock import patch
import random
import string


class UserInteractionTest(TestCase):
    def setUp(self):
        random.seed(408245472491)

    def get_text_data(self):
        return ["{", "#", "''", "Cat", "dog", "BIRD", "-1^&&%SS", ""]

    def print_test(self, func, text, test_text=None):
        with patch("builtins.print") as mocked_print:
            if test_text != None:
                func(test_text)
            else:
                func()
            mocked_print.assert_called_with(text)

    def test_show_global_instant(self):
        test_text_list = self.get_text_data()
        for test_text in test_text_list:
            self.print_test(user_interaction.show_global_instant,
                            f"GLOBAL: {test_text}", test_text)

    def test_show_active_instant(self):
        test_text_list = self.get_text_data()
        for test_text in test_text_list:
            self.print_test(user_interaction.show_active_instant,
                            f"ACTIVE: {test_text}", test_text)

    def test_show_passive_instant(self):
        test_text_list = self.get_text_data()
        for test_text in test_text_list:
            self.print_test(user_interaction.show_passive_instant,
                            f"PASSIVE: {test_text}", test_text)

    def test_show_all(self):
        test_text_list = self.get_text_data()

        user_interaction.save_global(test_text_list[0])
        user_interaction.save_active(test_text_list[1])
        user_interaction.save_passive(test_text_list[2])
        user_interaction.save_passive(test_text_list[3])
        user_interaction.save_passive(test_text_list[4])
        user_interaction.save_global(test_text_list[5])
        user_interaction.save_active(test_text_list[6])
        user_interaction.save_global(test_text_list[7])

        asserted_text = f"{user_interaction.MessageScope.PASSIVE.name}: {str(test_text_list[2:5])}"

        self.print_test(user_interaction.show_all, asserted_text)

    def test_read_index(self):
        for i in range(100):
            valid_test_data_list = [random.randint(1, 1000), 0]
            for test_data_item in valid_test_data_list:
                print(test_data_item)
                test_to_string = str(test_data_item)

                with patch('builtins.input', return_value=test_to_string):
                    self.assertEqual(user_interaction.read_index(
                        test_to_string), test_data_item)

        for i in range(100):
            invalid_test_data_list = [random.randint(-1000, -1), *self.get_text_data(), random.random(), random.choice([
                True, False]), None]
            for test_data_item in invalid_test_data_list:
                test_to_string = str(test_data_item)
                print(test_to_string)

                with patch('builtins.input', return_value=test_to_string):
                    self.assertEqual(user_interaction.read_index(
                        test_to_string), None)
