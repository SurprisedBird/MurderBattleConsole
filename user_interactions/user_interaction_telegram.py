from user_interactions.base_user_interaction import (BaseUserInteraction,
                                                     MessageScope)
import telebot
from typing import Optional
import time
import message_text_config as msg

token = "1608802403:AAELfG3U92U9XSQPqn5QdGxwTEZyLzULDUc"


class UserInteraction(BaseUserInteraction):
    def __init__(self, context: 'Context'):
        super().__init__(context)
        self.index = ""
        self.bot = telebot.TeleBot(token=token)

    def send(self, msg, chat_id, token=token, reply_markup=None):
        if msg and msg is not "\n":
            self.bot.send_message(
                chat_id=chat_id, text=msg, reply_markup=reply_markup)

    def show_global_instant(self, text: str) -> None:
        self.send(text, self.users[0].id)
        self.send(text, self.users[1].id)

    def show_active_instant(self, text: str) -> None:
        self.send(text, self.context.city.active_player.user.id)

    def show_passive_instant(self, text: str) -> None:
        self.send(text, self.context.city.passive_player.user.id)

    def show_all(self) -> None:
        for scope, text_list in self._prepared_messages.items():
            for text in text_list:
                if scope is MessageScope.GLOBAL:
                    self.send(
                        text, self.context.city.active_player.user.id)
                    self.send(
                        text, self.context.city.passive_player.user.id)
                elif scope is MessageScope.ACTIVE:
                    self.send(
                        text, self.context.city.active_player.user.id)
                elif scope is MessageScope.PASSIVE:
                    self.send(
                        text, self.context.city.passive_player.user.id)

        self._clear_messages()

    def read_number(self, text: str = "") -> Optional[int]:
        """Reading and validating inputs.

        If input value is valid - return int
        If input value is NOT valid - return None
        """

        self.send(text, self.context.city.active_player.user.id)

        @self.bot.message_handler(commands=['help'])
        def help(message):
            text = "Чтобы получить информацию обо всех картах введите команду /cards.\n Чтобы получить информацию о конкретной карте: напишите название карты или имя владельца этой карты"
            self.bot.send_message(message.chat.id, text)

        @self.bot.message_handler(commands=['cards'])
        def help(message):
            text = "СПИСОК КАРТ И ЖИТЕЛЕЙ, КОТОРЫЕ ЯВЛЯЮТСЯ ИХ ВЛАДЕЛЬЦАМИ:\n\n\n"
            for citizen, card in zip(msg.Help.CITIZENS.keys(), msg.Help.CARDS.keys()):
                text += f"{card} ({citizen}): {msg.Help.CITIZENS[citizen]}\n\n"

            self.bot.send_message(message.chat.id, text)

        @self.bot.message_handler(content_types=["text"])
        def input_messages(message):
            index_str = message.text
            if index_str in msg.Help.CITIZENS.keys():
                self.bot.send_message(
                    message.chat.id, msg.Help.CITIZENS[message.text])

            if index_str in msg.Help.CARDS.keys():
                self.bot.send_message(
                    message.chat.id, msg.Help.CARDS[message.text])

            if index_str.isnumeric():
                self.index = int(index_str)
                self.bot.stop_polling()
                return self.index
            else:
                index = None

        self.bot.polling(interval=1, timeout=1)
        return self.index
