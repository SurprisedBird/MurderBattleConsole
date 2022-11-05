from re import S
from user_interactions.base_user_interaction import (BaseUserInteraction,
                                                     MessageScope)
import telebot
from typing import Optional
import time
import message_text_config as msg

import asyncio
from email import message
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

#token = "1608802403:AAELfG3U92U9XSQPqn5QdGxwTEZyLzULDUc"
token = "5413116216:AAGN7T5uYSQl3BdmzBVbZD_ml0zgcWPt3a8"

class UserInteraction(BaseUserInteraction):
    def __init__(self, context: 'Context'):
        super().__init__(context)
        self.index = ""
        self.bot = telebot.TeleBot(token=token)
        self.game_log = []

    def send(self, msg, chat_id, token=token, reply_markup=None):
        if msg and msg != "\n":
            self.game_log.append(msg)
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
            global_text = ""
            active_text = ""
            passive_text = ""

            for text in text_list:
                if scope is MessageScope.GLOBAL:
                    global_text += f"{text}\n"
                elif scope is MessageScope.ACTIVE:
                    active_text += f"{text}\n"
                elif scope is MessageScope.PASSIVE:
                    passive_text += f"{text}\n"

            self.send(global_text, self.context.city.active_player.user.id)
            self.send(global_text, self.context.city.passive_player.user.id)
            self.send(active_text, self.context.city.active_player.user.id)
            self.send(passive_text, self.context.city.passive_player.user.id)

        self._clear_messages()

    def read_note(self):
        
        #API_TOKEN = "1608802403:AAELfG3U92U9XSQPqn5QdGxwTEZyLzULDUc"
        API_TOKEN = "5413116216:AAGN7T5uYSQl3BdmzBVbZD_ml0zgcWPt3a8"
        loop = asyncio.get_event_loop()
        bot = Bot(token=API_TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)

        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)
        dp.middleware.setup(LoggingMiddleware())

        async def start_noting():
            await bot.send_message(self.context.city.active_player.user.id, msg.CommonMessages.NOTICE)
            
        @dp.message_handler(content_types=["text"])
        async def save_notice(message):
            if message.text == "Нет":
                self.context.city.active_player.active_note = ""
            else:
                self.context.city.active_player.active_note = message.text
            loop.stop()

        executor.start(dp, start_noting())
        executor.start_polling(dp, loop=loop, skip_updates=True)

    def read_number(self, text: str = "") -> Optional[int]:
        """Reading and validating inputs.

        If input value is valid - return int
        If input value is NOT valid - return None
        """

        self.index = 0
        #self.send(text, self.context.city.active_player.user.id)
        if text != "":
            self.save_active(text)
        
        #API_TOKEN = "1608802403:AAELfG3U92U9XSQPqn5QdGxwTEZyLzULDUc"
        API_TOKEN = "5413116216:AAGN7T5uYSQl3BdmzBVbZD_ml0zgcWPt3a8"
        loop = asyncio.get_event_loop()
        bot = Bot(token=API_TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)

        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)
        dp.middleware.setup(LoggingMiddleware())

        keyboard = types.InlineKeyboardMarkup(row_width=4, one_time_keyboard=True)
        inline_btns = []
        for i in range(0, 13):
            inline_btns.append(types.InlineKeyboardButton(i, callback_data=i))
        
        keyboard.row(inline_btns[0])
        keyboard.row(inline_btns[1], inline_btns[2], inline_btns[3], inline_btns[4])
        keyboard.row(inline_btns[5], inline_btns[6], inline_btns[7], inline_btns[8])
        keyboard.row(inline_btns[9], inline_btns[10], inline_btns[11], inline_btns[12])

        async def open_keyboard():
            await bot.send_message(self.context.city.active_player.user.id, self.history[MessageScope.ACTIVE][-1], reply_markup=keyboard)
            self._clear_messages()
            
        @dp.message_handler(commands=['cards'])
        async def cards(message):
            text = "СПИСОК КАРТ И ЖИТЕЛЕЙ, КОТОРЫЕ ЯВЛЯЮТСЯ ИХ ВЛАДЕЛЬЦАМИ:\n\n\n"
            for citizen, card in zip(msg.Help.CITIZENS.keys(), msg.Help.CARDS.keys()):
                text += f"{card} ({citizen}): {msg.Help.CITIZENS[citizen]}\n\n"

            await bot.send_message(message.chat.id, text)

        @dp.callback_query_handler(lambda message: True)
        async def get_number(call: types.CallbackQuery):
            self.index = int(call.data)
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            loop.stop()

        executor.start(dp, open_keyboard())
        executor.start_polling(dp, loop=loop, skip_updates=True)
        return self.index
