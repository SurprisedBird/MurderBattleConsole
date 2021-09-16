from enum import Enum, auto

from card import Card
from effects.alarm_effect import AlarmEffect
from effects.anonymus_call_effect import AnonymusCallEffect
from effects.antidot_effect import AntidotEffect
from effects.database_effect import DatabaseEffect
from effects.freak_effect import FreakEffect
from effects.gang_effect import GangEffect
from effects.gossips_effect import GossipsEffect
from effects.taxes_effect import TaxesEffect
from effects.theatre_effect import TheatreEffect
from effects.trap_effect import TrapEffect
from effects.videocamera_effect import VideoCameraEffect
from effects.whore_effect import WhoreEffect
from effects.witness_effect import WitnessEffect
from game_controller import GameController
from telegram_initializer import TelegramInitializer

cards = {
    "База данных": Card("База данных", DatabaseEffect),
    "Сплетни": Card("Сплетни", GossipsEffect),
    "Видеокамера": Card("Видеокамера", VideoCameraEffect),
    "Система тревоги": Card("Система тревоги", AlarmEffect),
    "Ловушка": Card("Ловушка", TrapEffect),
    "Защита свидетеля": Card("Защита свидетеля", WitnessEffect),
    "Наркотики": Card("Наркотики", FreakEffect),
    "Анонимный звонок": Card("Анонимный звонок", AnonymusCallEffect),
    "Театральный реквизит": Card("Театральный реквизит", TheatreEffect),
    "Проститутка": Card("Проститутка", WhoreEffect),
    "Налоги": Card("Налоги", TaxesEffect),
    "Антидот": Card("Антидот", AntidotEffect),
    "Банда": Card("Банда", GangEffect),
}

citizens_dict = [
    {"name": "Мальчик Хакер", "role": "C", "hp": 1,
        "card": cards["База данных"], "stolen_cards": []},

    {"name": "Ночная продавщица", "role": "C", "hp": 1,
        "card": cards["Сплетни"], "stolen_cards": []},

    {"name": "Начальник охраны", "role": "C", "hp": 1,
        "card": cards["Видеокамера"], "stolen_cards": []},

    {"name": "Надзиратель", "role": "P1", "hp": 3,
        "card": cards["Система тревоги"], "stolen_cards": []},

    {"name": "Охотник", "role": "P2", "hp": 3,
        "card": cards["Ловушка"], "stolen_cards": []},

    {"name": "Полицейский", "role": "C", "hp": 1,
        "card": cards["Защита свидетеля"], "stolen_cards": []},

    {"name": "Наркоман", "role": "C", "hp": 1,
        "card": cards["Наркотики"], "stolen_cards": []},

    {"name": "Вечно недовольная старушка", "role": "S", "hp": 1,
        "card": cards["Анонимный звонок"], "stolen_cards": []},

    {"name": "Актер", "role": "C", "hp": 1,
        "card": cards["Театральный реквизит"], "stolen_cards": []},

    {"name": "Сутенер", "role": "C", "hp": 1,
        "card": cards["База данных"], "stolen_cards": []},

    {"name": "Соцработник", "role": "C", "hp": 1,
        "card": cards["Налоги"], "stolen_cards": []},

    {"name": "Врач", "role": "C", "hp": 1,
        "card": cards["Антидот"], "stolen_cards": []},

    {"name": "Бригадир", "role": "C", "hp": 1,
        "card": cards["Банда"], "stolen_cards": []},
]

if __name__ == "__main__":
    while(True):
        tel = TelegramInitializer()

        users = tel.get_users()

        gc = GameController(citizens_dict, users)

        gc.start_game()
