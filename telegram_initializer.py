import telebot
from user import User
import message_text_config as msg


class TelegramInitializer:
    def __init__(self):
        self.token = "1608802403:AAELfG3U92U9XSQPqn5QdGxwTEZyLzULDUc"
        self.bot = telebot.TeleBot(token=self.token)
        self.users = []

    def get_users(self):
        @self.bot.message_handler(commands=['join'])
        def join(message):
            if len(self.users) == 2:
                self.bot.send_message(
                    message.chat.id, text="Комната переполнена!")
                return

            users_ids = []
            for user in self.users:
                users_ids.append(user.id)

            if message.chat.id not in users_ids:
                self.users.append(User(
                    message.chat.username, message.chat.id))
                self.bot.send_message(
                    message.chat.id, text="Спасибо за регистрацию")
                return
            else:
                self.bot.send_message(
                    message.chat.id, text="Этот пользователь уже в игре")

        @ self.bot.message_handler(commands=['quit'])
        def quit(message):
            for user in self.users:
                if user.id == message.chat.id:
                    self.users.remove(user)
                    self.bot.send_message(
                        message.chat.id, text="Вы вышли из комнаты!")
                return

            self.bot.send_message(
                message.chat.id, text="Вы еще не вошли в игру")

        @self.bot.message_handler(commands=['show_players'])
        def show_players(message):
            for user in self.users:
                self.bot.send_message(
                    message.chat.id, text=f"Name = {user.name}, ID = {user.id}")

            if len(self.users) == 0:
                self.bot.send_message(
                    message.chat.id, text="Игроки не обнаружены")

        @self.bot.message_handler(commands=['go'])
        def go(message):
            if len(self.users) == 2:
                self.bot.stop_polling()

                return self.users
            else:
                self.bot.send_message(
                    message.chat.id, text="Недостаточно игроков для начала игры")

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
        def get_info(message):
            if message.text in msg.Help.CITIZENS.keys():
                self.bot.send_message(
                    message.chat.id, msg.Help.CITIZENS[message.text])

            if message.text in msg.Help.CARDS.keys():
                self.bot.send_message(
                    message.chat.id, msg.Help.CARDS[message.text])

        self.bot.polling(interval=1, timeout=1)

        return self.users
