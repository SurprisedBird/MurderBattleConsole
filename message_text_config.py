class CommonMessages:
    ERROR_INVALID_TARGET = "Ошибка! Введите номер доступной цели."
    ERROR_SELF_AS_TARGET = "Ошибка! Невозможно выбрать себя в качестве цели."
    LOST_HP = "Вы потеряли 1 HP"


# ------------------------------------------------------
# Effect messages
# ------------------------------------------------------


class StealMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите цель, которую вы попытаетесь ограбить в эту ночь:"
    ACTIVATION_SUCCESS = "Дом гражданина {} будет ограблен."
    RESOLVE_SUCCESS = "Вы получили карту {}."
    RESOLVE_FAILED = "Вы проникли в дом {}, но карту обнаружить вам не удалось."
    RESOLVE_LOST_CARD = "Ваша карта была украдена"


class KillMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите цель, на которую будет совершено покушение на убийство в эту ночь:"
    RESOLVE_SUCCESS = "Ночь была неспокойной. Был хладнокровно убит {}. Весь город скорбит."
    RESOLVE_NO_CARD = "Карту обнаружить вам не удалось."
    RESOLVE_FAILED = "Ночь была неспокойной. Было совершено покушение на гражданина {}. Гражданин {} выжил благодаря чуду."
    RESOLVE_ENEMY_LOST_HP = CommonMessages.LOST_HP
    ERROR_INVALID_TARGET = CommonMessages.ERROR_INVALID_TARGET
    ERROR_SELF_AS_TARGET = CommonMessages.ERROR_SELF_AS_TARGET
    # RESOLVE_KILL_SPY = "Ночь была неспокойной. Гражданин {} оказался не тем за кого себя выдавал. Шпион, который скрывался под личиной гражданина {}, в спешке покинул город."


class StagingMassages:
    ACTIVATION_CHOOSE_TARGET = "Выберите цель, с которой вы поменяетесь ролями в эту ночь (в новостях объявят о гибели гражданина с вашей предыдущей ролью):"
    ACTIVATION_SUCCESS = "После совершения инсценировки, вы окажетесь в роли {}."
    RESOLVE_SUCCESS = "Инсценировка удалась, ваша новая роль {}."
    RESOLVE_FAILED = "Вам не удалось инсценировать свою смерть, но вы нанесли урон цели."
    RESOLVE_ENEMY_LOST_HP = CommonMessages.LOST_HP
    ERROR_INVALID_TARGET = CommonMessages.ERROR_INVALID_TARGET
    ERROR_SELF_AS_TARGET = CommonMessages.ERROR_SELF_AS_TARGET


class AlarmMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, на дом которого будет установлена Система Тревоги:"
    ACTIVATION_SUCCESS = "Система тревоги была установлена на дом гражданина - {}."
    RESOLVE_FORCED_TO_RUN = "Вы активировали Систему Тревоги, поэтому были вынуждены броситься в бегство."
    RESOLVE_ALARM_ACTIVATED = "Система тревоги была активирована."


class DatabaseMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите одну из трех целей, которые будут проанализированы с помощью базы данных:"
    RESOLVE_FIND_ALL = "База данных показала, что среди указанных граждан есть Убийца и Шпион."
    RESOLVE_FIND_PLAYER = "База данных показала, что среди указанных граждан есть Убийца."
    RESOLVE_FIND_SPY = "База данных показала, что среди указанных граждан есть Шпион."
    RESOLVE_NO_SUSPECT = "База данных показала, что среди указанных граждан нет подозрительных личностей."
    ERROR_INVALID_TARGET = CommonMessages.ERROR_INVALID_TARGET
    ERROR_SAME_TARGET = "Ошибка! Все цели должны быть разными."


class VideoCameraMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, на дом которого будет установлена Видеокамера:"
    ACTIVATION_SUCCESS = "Видеокамера была установлена на дом гражданина - {}."
    RESOLVE_SUCCESS = "Видеокамера зафиксировала как {} вломился в дом {}."


class WhoreMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, которого сегодня посетит Жрица Любви:"
    ACTIVATION_SUCCESS = "Жрица Любви отправилась в дом гражданина - {}."
    RESOLVE_START_PUBLICLY = "На охоту вышла Ночная Бабочка, готовая, следующей ночью, одарить одного из горожан своим визитом."
    RESOLVE_SUCCESS = "Следующую ночь вы проведете с очаровательной красоткой и не сможете совершать действие Убийства, Кражи или Инсценировки."


class TrapMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, на дом которого будет установлена Ловушка:"
    ACTIVATION_SUCCESS = "Ловушка была установлена на дом гражданина - {}."
    RESOLVE_SUCCESS = "В дом {} вломился неизвестный, но оказался в западне."
    RESOLVED_CATCHED = "Вы попали в Ловушку, ваше действие было прервано."


class WitnessDefendMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, на дом которого будет установлена Защита свидетеля:"
    ACTIVATION_SUCCESS = "Защита свидетеля была установлена на дом гражданина - {}."
    RESOLVE_START_PUBLICLY = "Городская полиция оцепила один из домов. Говорят, что они нашли ценного свидетеля по делу городских убийств."
    RESOLVE_SUCCESS_PUBLICLY = "В дом {} вломился неизвестный, но был остановлен доблестными стражами закона."


class TheatreMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, роль которого будет теперь отображаться вместо вашей при анализе с помощью эффектов обнаружения:"
    ACTIVATION_SUCCESS = "Вы успешно использовали театральный реквизит. Ваша новая роль - {}. Сыграйте ее достойно!"


class TalesMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите ночь, информация о которой будет предоставлена:"
    RESOLVE_SUCCESS = "В этот ход противник сделал следующее: {}"
    ERROR_INVALID_TARGET = "Ошибка! Целью для карты Сплетни является номер ночи. Введите номер доступной ночи."


class DrugsMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, к дому которого будет отправлен Наркоман:"
    RESOLVE_SUCCESS = "Наркоман успешно устроил диверсию в доме гражданина - {}."


class AnonymousCallMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, которого сегодняшней ночью неизвестный обвинит с помощью анонимного звонка в полицию:"
    RESOLVE_SUCCESS = "В полицию поступил загадочный анонимный звонок, где высказывались обвинения в убийстве с указанием конкретного подозреваемого. Полиция решила перепроверить данную информацию"
    RESOLVE_ANONYMOUSCALL_NO_SUSPECT = "Полиция проверила дом гражданина - {}. Достоверно, что он не является подозрительным."
    RESOLVE_ANONYMOUSCALL_PLAYER = "Полиция проверила дом гражданина - {}. Достоверно, что он является Убийцей."
    RESOLVE_ANONYMOUSCALL_SPY = "Полиция проверила дом гражданина - {}. Достоверно, что он является Шпионом."


class TaxesMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, которого сегодня посетит Соцработник:"
    ACTIVATION_SUCCESS = "Вы отправили Соцработника в дом гражданина - {}."
    RESOLVE_PLAYER_CHOOSE_VARIANT = "Этой ночью вас посетил жадный Соцработник. Выберите способ откупиться от него: \n [{}, 2.HP]"
    RESOLVE_PLAYER_CHOOSE_CARD = "Выберите карту: \n {}"
    RESOLVE_SUCCESS = "Соцработник покинул вас, доставив немало хлопот."


class AntidoteMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите гражданина, который следующий ход будет защищен от смертельной атаки:"
    ACTIVATION_SUCCESS = "Вы использовали Антидот на гражданина - {}."
    RESOLVE_SUCCESS = "Препарат нового поколения спас гражданина {} от неминуемой смерти"


class GangMessages:
    ACTIVATION_SUCCESS = "Банда вышла на охоту и следующий ход никто не посмеет помешать вашим планам."
    RESOLVE_SUCCESS = "Банда изрядно поколотила вас в эту ночь, не дав возможность осуществить задуманное."


class GossipsMessages:
    ACTIVATION_CHOOSE_TARGET = "Выберите ночь о которой поведает ночная продавщица:"
    RESOLVE_SUCCESS = "В эту ночь убийца совершил следующие действия:\n {}, цель: {}\n {}, цель: {}"


# ------------------------------------------------------
# Player messages
# ------------------------------------------------------


class PlayerMessages:
    ACTION_NONE = "Пропустить"
    ACTION_STEAL = "Украсть"
    ACTION_KILL = "Убить"
    ACTION_STAGING = "Совершить инсценировку"
    ACTION_CARD_USAGE = "Использовать карту"
    ERROR_ACTION_CHOICE = "Ошибка! Введите номер доступного действия."
    ERROR_CARD_ACTION_CHOICE = "Ошибка! Введите номер доступной карты."
    CHOOSE_ACTION = "Введите номер действия:"
    OPTION = "{}. {}"
    CHOOSE_CARD_ACTION = "Введите номер карты:"


# ------------------------------------------------------
# GameController messages
# ------------------------------------------------------


class PreparePhase:
    GLOBAL_LOAD_GAME = "Загрузка игры"
    GLOBAL_FIRST_TURN = "Первым будет ходить {}"
    ACT_FIRST_TURN = "Вы будете ходить первым"
    ACT_PASS_YOUR_ROLE = "Ваша роль – {}. Ваша задача, обнаружить вашего противника и нейтрализовать его раньше, чем это сделает он. Будьте расчетливым, непредсказуемым и коварным убийцей. Удачи!"
    GLOBAL_START_GAME = "Игра началась!"


class FinishPhase:
    GLOBAL_DRAW = "Ничья!"
    GLOBAL_PLAYER_WON = "Игрок {} победил"


class NightState:
    NIGHT_NUMBER = "НОЧЬ {}"
    ENEMY_TURN = "Ход противника"
    YOUR_TURN = "Ваш ход"
    HP_COUNT = "HP = {}"
    IS_STAGING = "Наличие Инсценировки: {}"
    STAGING_AVAILABLE = "присутствует"
    STAGING_UNAVAILABLE = "отсутствует"
    PERSONAL_CARD = "Личная карта: {}"
    NO_CARD = " - "
    STOLEN_CARDS = "Украденные карты:\n {}"
    CITY_STATUS = "Город:\n {}"
    CITIZEN_LIST_OPTION = "{}. {} {}"
    YOU = "(Вы)"
    DEAD = "(мертв)"


class NightActionTarget:
    ACT_CHOISE_INFO = "Вы выбрали действие '{}'. Вы выбрали карту '{}'."
    ACT_CONFIRM_ACTION = "Подтвердить действие"
    ACT_CANCEL_ACTION = "Отменить действие"


class DayGeneral:
    GLOBAL_DAY_NUMBER = "ДЕНЬ {}"
    GLOBAL_STEAL_CITIZEN = "Эта ночь прошла спокойно."
    # Commonly used
    # ACT_PASS_LOST_HP = "Вы потеряли 1 HP"


class FinishTurn:
    ACT_FINISH_TURN = "Ваш ход завершен!"


class Errors:
    # Commonly used
    # TARGET = "Ошибка! Введите номер доступной цели."
    # CARDS_ONE_TARGET = "Ошибка! Введите одну цель для выбранной карты."
    # DATA_BASE_TARGETS = "Ошибка! Введите три цели для выбранной карты."
    CONFIRM_CHOICE = "Ошибка! Введите номер доступного действия."
