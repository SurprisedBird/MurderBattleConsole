import telebot
from user import User


class TelegramInitializer:
    def __init__(self):
        self.token = "1608802403:AAELfG3U92U9XSQPqn5QdGxwTEZyLzULDUc"
        self.bot = telebot.TeleBot(token=self.token)
        self.first_user = None
        self.second_user = None
        self.users = []

    def get_users(self):
        @self.bot.message_handler(commands=['create'])
        def create(message):
            if self.first_user is None:
                self.first_user = User(message.chat.username, message.chat.id)
            else:
                if message.chat.id != self.first_user.id:
                    self.second_user = User(
                        message.chat.username, message.chat.id)
                else:
                    self.bot.send_message(
                        message.chat.id, text="Этот пользователь уже в игре")
            self.bot.send_message(
                message.chat.id, text="Спасибо за регистрацию")

        @self.bot.message_handler(commands=['show_players'])
        def show_players(message):
            if self.first_user is not None:
                self.bot.send_message(
                    message.chat.id, text=f"Name = {self.first_user.name}, ID = {self.first_user.id}")
            if self.second_user is not None:
                self.bot.send_message(
                    message.chat.id, text=f"Name = {self.second_user.name}, ID = {self.second_user.id}")
            if self.first_user is None and self.second_user is None:
                self.bot.send_message(
                    message.chat.id, text="Игроки не обнаружены")

        @self.bot.message_handler(commands=['start_game'])
        def start_game(message):
            if self.first_user is not None and self.second_user is not None:
                self.bot.stop_polling()
                self.users.append(self.first_user)
                self.users.append(self.second_user)
                return self.users
            else:
                self.bot.send_message(
                    message.chat.id, text="Недостаточно игроков для начала игры")

        self.bot.polling(interval=1, timeout=1)

        return self.users
