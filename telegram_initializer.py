import telebot
from user import User
import message_text_config as msg

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
import asyncio

class TelegramInitializer:
    def __init__(self):
        self.users = []
        
        API_TOKEN = "1608802403:AAELfG3U92U9XSQPqn5QdGxwTEZyLzULDUc"
        self.loop = asyncio.get_event_loop()
        self.bot = Bot(token=API_TOKEN, loop=self.loop, parse_mode=types.ParseMode.HTML)

        storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=storage)
        self.dp.middleware.setup(LoggingMiddleware())

    def get_users(self):
        @self.dp.message_handler(commands='join')
        async def join_player(message: types.Message):
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
                await self.bot.send_message(
                    message.chat.id, text="Спасибо за регистрацию")
                return
            else:
                await self.bot.send_message(
                    message.chat.id, text="Этот пользователь уже в игре")

        @self.dp.message_handler(commands=['quit'])
        async def quit(message):
            for user in self.users:
                if user.id == message.chat.id:
                    self.users.remove(user)
                    await self.bot.send_message(
                        message.chat.id, text="Вы вышли из комнаты!")
                return

            await self.bot.send_message(
                message.chat.id, text="Вы еще не вошли в игру")

        @self.dp.message_handler(commands=['show_players'])
        async def show_players(message):
            for user in self.users:
                await self.bot.send_message(
                    message.chat.id, text=f"Name = {user.name}, ID = {user.id}")

            if len(self.users) == 0:
                await self.bot.send_message(
                    message.chat.id, text="Игроки не обнаружены")

        @self.dp.message_handler(commands=['go'])
        async def go(message):
            if len(self.users) == 2:
                self.loop.stop()

                return self.users
            else:
                await self.bot.send_message(
                    message.chat.id, text="Недостаточно игроков для начала игры")
                
        @self.dp.message_handler(commands=['help'])
        async def help(message):
            text = "Чтобы получить информацию обо всех картах введите команду /cards.\n Чтобы получить информацию о конкретной карте: напишите название карты или имя владельца этой карты"
            await self.bot.send_message(message.chat.id, text)

        @self.dp.message_handler(commands=['cards'])
        async def help(message):
            text = "СПИСОК КАРТ И ЖИТЕЛЕЙ, КОТОРЫЕ ЯВЛЯЮТСЯ ИХ ВЛАДЕЛЬЦАМИ:\n\n\n"
            for citizen, card in zip(msg.Help.CITIZENS.keys(), msg.Help.CARDS.keys()):
                text += f"{card} ({citizen}): {msg.Help.CITIZENS[citizen]}\n\n"

            await self.bot.send_message(message.chat.id, text)

        @self.dp.message_handler(content_types=["text"])
        async def get_info(message):
            if message.text in msg.Help.CITIZENS.keys():
                await self.bot.send_message(
                    message.chat.id, msg.Help.CITIZENS[message.text])

            if message.text in msg.Help.CARDS.keys():
                await self.bot.send_message(
                    message.chat.id, msg.Help.CARDS[message.text])

        executor.start_polling(self.dp, loop=self.loop, skip_updates=True)
        return self.users
