from enum import Enum, auto

from card import Card
from effects.alarm_effect import AlarmEffect
from effects.database_effect import DatabaseEffect
from effects.gossips_effect import GossipsEffect
from effects.none_effect import NoneEffect
from effects.trap_effect import TrapEffect
from effects.videocamera_effect import VideoCameraEffect
from effects.whore_effect import WhoreEffect
from game_controller import GameController

citizens_dict = {
    "Мальчик Хакер": Card("База данных", DatabaseEffect),
    "Ночная продавщица": Card("Сплетни", GossipsEffect),
    "Начальник охраны": Card("Видеокамера", VideoCameraEffect),
    "Сутенер": Card("Проститутка", WhoreEffect),
    "Надзиратель": Card("Система тревоги", AlarmEffect),
    "Охотник": Card("Ловушка", TrapEffect),
    "Полицейский": Card("Защита свидетеля", NoneEffect),
    "Актер": Card("Театральный реквизит", NoneEffect),
    "Наркоман": Card("Наркотики", NoneEffect),
    "Вечно недовольная старушка": Card("Анонимный звонок", NoneEffect),
    "Соцработник": Card("Налоги", NoneEffect),
    "Врач": Card("Антидот", NoneEffect),
    "Бригадир": Card("Банда", NoneEffect)
}

user_names = ["GvinP", "Runmaget"]

if __name__ == "__main__":
    gc = GameController(citizens_dict, user_names)

    gc.start_game()
