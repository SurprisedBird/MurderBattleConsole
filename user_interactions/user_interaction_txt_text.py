import os
from datetime import datetime

from user_interactions.base_user_interaction import (BaseUserInteraction,
                                                     MessageScope)


class FileManager():
    def __init__(self, history_dir: str) -> None:
        self.root_dir = os.path.dirname(__file__)
        self.history_dir = os.path.join(self.root_dir, history_dir)

        if not os.path.exists(self.history_dir):
            os.mkdir(self.history_dir)

        current_date = datetime.now().strftime('%Y-%m-%d-%H.%M.%S')
        self.dir = os.path.join(self.history_dir, f"Game-{current_date}")
        os.mkdir(self.dir)

    def update_history_text(self, player_name, text):
        self.file_dir = f"{self.dir}/{player_name}.txt"
        with open(self.file_dir, mode='a') as file:
            file.write(text + '\n')


class UserInteraction(BaseUserInteraction):
    def __init__(self, context: 'Context'):
        super().__init__(context)
        self.file_manager = FileManager("History")
        self.game = self.context.game

    def show_global_instant(self, text: str) -> None:
        print(f"{MessageScope.GLOBAL.name}: {text}")
        self.file_manager.update_history_text(self.user_names[0], text)
        self.file_manager.update_history_text(self.user_names[1], text)

    def show_active_instant(self, text: str) -> None:
        print(self.user_names[0])
        print(f"{MessageScope.ACTIVE.name}: {text}")
        self.file_manager.update_history_text(
            self.game.active_player.user_name, text)

    def show_passive_instant(self, text: str) -> None:
        print(self.user_names[1])
        print(f"{MessageScope.PASSIVE.name}: {text}")
        self.file_manager.update_history_text(
            self.game.passive_player.user_name, text)

    def show_all(self) -> None:
        for scope, text_list in self._prepared_messages.items():
            print(f"{scope.name}:")
            for text in text_list:
                print(f"\t{text}")
                if scope == MessageScope.GLOBAL:
                    self.file_manager.update_history_text(
                        self.game.active_player.user_name, text)
                    self.file_manager.update_history_text(
                        self.game.passive_player.user_name, text)

                elif scope == MessageScope.ACTIVE:
                    self.file_manager.update_history_text(
                        self.game.active_player.user_name, text)

                else:
                    self.file_manager.update_history_text(
                        self.game.passive_player.user_name, text)

        self._clear_messages()
