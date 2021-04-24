from user_interactions.base_user_interaction import (BaseUserInteraction,
                                                     MessageScope)
import telebot
from typing import Optional
import time

token = "1608802403:AAELfG3U92U9XSQPqn5QdGxwTEZyLzULDUc"


class UserInteraction(BaseUserInteraction):
    def __init__(self, context: 'Context'):
        super().__init__(context)
        self.index = ""
        self.bot = telebot.TeleBot(token=token)

    def send(self, msg, chat_id, token=token):
        if msg and msg is not "\n":
            self.bot.send_message(chat_id=chat_id, text=msg)

    def show_global_instant(self, text: str) -> None:
        self.send(text, self.user_names[0].id)
        self.send(text, self.user_names[1].id)

    def show_active_instant(self, text: str) -> None:
        self.send(text, self.context.city.active_player.user_name.id)

    def show_passive_instant(self, text: str) -> None:
        self.send(text, self.context.city.passive_player.user_name.id)

    def show_all(self) -> None:
        for scope, text_list in self._prepared_messages.items():
            for text in text_list:
                if scope is MessageScope.GLOBAL:
                    self.send(
                        text, self.context.city.active_player.user_name.id)
                    self.send(
                        text, self.context.city.passive_player.user_name.id)
                elif scope is MessageScope.ACTIVE:
                    self.send(
                        text, self.context.city.active_player.user_name.id)
                elif scope is MessageScope.PASSIVE:
                    self.send(
                        text, self.context.city.passive_player.user_name.id)

        self._clear_messages()

    def read_number(self, text: str = "") -> Optional[int]:
        """Reading and validating inputs.

        If input value is valid - return int
        If input value is NOT valid - return None
        """

        self.send(text, self.context.city.active_player.user_name.id)

        @self.bot.message_handler(content_types=["text"])
        def repeat_all_messages(message):
            index_str = message.text
            if index_str.isnumeric():
                self.index = int(index_str)
                self.bot.stop_polling()
                return self.index
            else:
                index = None

        self.bot.polling(interval=1, timeout=1)
        return self.index
