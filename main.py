from enum import Enum, auto

from card import Card
from effects.alarm_effect import AlarmEffect
from effects.anonymus_call_effect import AnonymusCallEffect
from effects.antidot_effect import AntidotEffect
from effects.database_effect import DatabaseEffect
from effects.freak_effect import FreakEffect
from effects.gang_effect import GangEffect
from effects.gossips_effect import GossipsEffect
from effects.none_effect import NoneEffect
from effects.taxes_effect import TaxesEffect
from effects.trap_effect import TrapEffect
from effects.videocamera_effect import VideoCameraEffect
from effects.whore_effect import WhoreEffect
from effects.witness_effect import WitnessEffect
from game_controller import GameController

citizens_dict = {
    "Мальчик Хакер": Card("База данных", DatabaseEffect),
    "Ночная продавщица": Card("Сплетни", GossipsEffect),
    "Начальник охраны": Card("Видеокамера", VideoCameraEffect),
    "Сутенер": Card("Проститутка", WhoreEffect),
    "Надзиратель": Card("Система тревоги", AlarmEffect),
    "Охотник": Card("Ловушка", TrapEffect),
    "Полицейский": Card("Защита свидетеля", WitnessEffect),
    "Актер": Card("Театральный реквизит", NoneEffect),
    "Наркоман": Card("Наркотики", FreakEffect),
    "Вечно недовольная старушка": Card("Анонимный звонок", AnonymusCallEffect),
    "Соцработник": Card("Налоги", TaxesEffect),
    "Врач": Card("Антидот", AntidotEffect),
    "Бригадир": Card("Банда", GangEffect)
}

user_names = ["GvinP", "Runmaget"]

if __name__ == "__main__":
    gc = GameController(citizens_dict, user_names)

    gc.start_game()
