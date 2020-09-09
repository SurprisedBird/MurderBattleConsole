class UserActions:
    TYPE_NONE = "Пропустить"
    TYPE_STEAL = "Украсть"
    TYPE_KILL = "Убить"
    TYPE_STAGING = "Совершить инсценировку"
    TYPE_CARD_USAGE = "Использовать карту"


class PreparePhase:
    GLOBAL_LOAD_GAME = "Загрузка игры"
    GLOBAL_FIRST_TURN = "Первым будет ходить {}"
    ACT_FIRST_TURN = "Вы будете ходить первым"
    ACT_PASS_YOUR_ROLE = "Ваша роль – {}. Ваша задача, обнаружить вашего противника и нейтрализовать его раньше, чем это сделает он. Будьте расчетливым, непредсказуемым и коварным убийцей. Удачи!"
    GLOBAL_START_GAME = "Игра началась!"


class FinishPhase:
    GLOBAL_DRAW = "Ничья!"
    GLOBAL_PLAYER_WON = "Игрок {} победил"


class NightStatus:
    ACT_PASS_NIGHT_NUMBER = "НОЧЬ {}"
    PASS_ENEMY_TURN = "Ход противника"
    ACT_YOUR_TURN = "Ваш ход"
    ACT_HP_COUNT = "HP = {}"
    ACT_IS_STAGING = "Наличие Инсценировки: {}"
    ACT_STAGING_AVAILABLE = "присутствует"
    ACT_STAGING_UNAVAILABLE = "отсутствует"
    ACT_PERSONAL_CARD = "Личная карта: {}"
    ACT_NO_CARD = " - "
    ACT_STOLEN_CARDS = "Украденные карты:\n {}"
    ACT_CITY_STATUS = "Город:\n {}"
    ACT_CITIZEN_LIST_OPTION = "{}. {} {}"
    ACT_YOU = "(Вы)"
    ACT_DEAD = "(мертв)"


class NightActionTarget:
    ACT_ACTION = "Введите номер действия:"
    ACT_OPTION = "{}. {}"
    ACT_KILL = "Выберите цель, на которую будет совершено покушение на убийство в эту ночь:"
    ACT_STEAL = "Выберите цель, которую вы попытаетесь ограбить в эту ночь:"
    ACT_STAGING = "Выберите цель, с которой вы поменяетесь ролями в эту ночь (в новостях объявят о гибели гражданина с вашей предыдущей ролью):"
    ACT_CARD = "Введите номер карты:"
    ACT_CHOISE_INFO = "Вы выбрали действие '{}'. Вы выбрали карту '{}'."
    ACT_CONFIRM_ACTION = "Подтвердить действие"
    ACT_CANCEL_ACTION = "Отменить действие"


class CardTarget:
    ACT_DATABASE = "Выберите три цели, которые будут проанализированы с помощью базы данных:"
    ACT_TALES = "Выберите ночь, информация о которой будет предоставлена:"
    ACT_CAMERA = "Выберите гражданина, на дом которого будет установлена Видеокамера:"
    ACT_BITCH = "Выберите гражданина, которого сегодня посетит Жрица Любви:"
    ACT_ALARM = "Выберите гражданина, на дом которого будет установлена Система Тревоги:"
    ACT_TRAP = "Выберите гражданина, на дом которого будет установлена Ловушка:"
    ACT_WITNESSDEF = "Выберите гражданина, на дом которого будет установлена Защита свидетеля:"
    ACT_THEATRESTUFF = "Выберите гражданина, роль которого будет теперь отображаться вместо вашей при анализе с помощью эффектов обнаружения:"
    ACT_DRUGS = "Выберите гражданина, к дому которого будет отправлен Наркоман:"
    ACT_ANONYMOUSCALL = "Выберите гражданина, которого сегодняшней ночью неизвестный обвинит с помощью анонимного звонка в полицию:"
    ACT_TAXES = "Выберите гражданина, которого сегодня посетит Соцработник:"
    ACT_ANTIDOTE = "Выберите гражданина, который следующий ход будет защищен от смертельной атаки:"
    ACT_GANG = "Банда вышла на охоту и следующий ход никто не посмеет помешать вашим планам."


class DayGeneral:
    GLOBAL_DAY_NUMBER = "ДЕНЬ {}"
    GLOBAL_KILL_CITIZEN = "Ночь была неспокойной. Был хладнокровно убит {}. Весь город скорбит."
    GLOBAL_STEAL_CITIZEN = "Эта ночь прошла спокойно."
    GLOBAL_KILL_PLAYER = "Ночь была неспокойной. Было совершено покушение на {}. {} чудом удалось спастись."
    ACT_PASS_LOST_HP = "Вы потеряли 1 HP"
    GLOBAL_KILL_SPY = "Ночь была неспокойной. {} оказался не тем за кого себя выдавал. Шпион, который скрывался под личиной {} в спешке покинул город."


class NightResult:
    ACT_STEAL_SUCCESSFULL = "Вы получили карту {}."
    ACT_STEAL_UNSUCCESSFULL = "Вы проникли в дом {}, но карту обнаружить вам не удалось."
    ACT_STAGING_CITIZEN = "Инсценировка удалась, ваша новая роль {}."
    ACT_STAGING_PLAYER = "К сожалению, вам не удалось инсценировать свою смерть, однако противник пострадал в ходе ваших действий."
    PASS_LOST_CARD = "Ваша карта была украдена"


class EffectsActivated:
    GLOBAL_BITCH = "На охоту вышла Ночная Бабочка, готовая, следующей ночью, одарить одного из горожан своим визитом."
    GLOBAL_WITNESSDEF = "Городская полиция оцепила один из домов. Говорят, что они нашли ценного свидетеля по делу городских убийств."
    GLOBAL_ANONYMOUSCALL = "В полицию поступил загадочный анонимный звонок, где высказывались обвинения в убийстве с указанием конкретного подозреваемого. Полиция решила перепроверить данную информацию"
    ACT_CAMERA = "Видеокамера была установлена на дом гражданина - {}."
    ACT_BITCH = "Жрица Любви отправилась в дом гражданина - {}."
    ACT_ALARM = "Система тревоги была установлена на дом гражданина - {}."
    ACT_TRAP = "Ловушка была установлена на дом гражданина - {}."
    ACT_WITNESSDEF = "Защита свидетеля была установлена на дом гражданина - {}."
    ACT_THEATRESTUFF = "Вы успешно использовали театральный реквизит. Ваша новая роль - {}."
    ACT_DRUGS = "Наркоман успешно устроил диверсию в доме гражданина - {}."
    ACT_TAXES = "Вы отправили Соцработника в дом гражданина - {}."
    ACT_ANTIDOTE = "Вы использовали Антидот на гражданина - {}."
    ACT_TAXES_PLAYER_CHOOSE_VARIANT = "Этой ночью вас посетил жадный Соцработник. Выберите способ откупиться от него: \n [{}, 2.HP]"
    ACT_TAXES_PLAYER_CHOOSE_CARD = "Выберите карту: \n {}"


class EffectsResolved:
    GLOBAL_TRAP = "В дом {} вломился неизвестный, но оказался в западне."
    GLOBAL_WITNESSDEF = "В дом {} вломился неизвестный, но был остановлен доблестными стражами закона."
    ACT_DATABASE_NO_SUSPECT = "База данных показала, что среди указанных граждан нет подозрительных личностей."
    ACT_DATABASE_FIND_PLAYER = "База данных показала, что среди указанных граждан есть Убийца."
    ACT_DATABASE_FIND_SPY = "База данных показала, что среди указанных граждан есть Шпион."
    ACT_DATABASE_FIND_ALL = "База данных показала, что среди указанных граждан есть Убийца и Шпион."
    ACT_TALES = "В этот ход противник сделал следующее: {}"
    ACT_CAMERA = "Видеокамера зафиксировала как {} вломился в дом {}."
    PASS_BITCH = "Следующую ночь вы проведете с очаровательной красоткой и не сможете совершать действие Убийства, Кражи или Инсценировки."
    PASS_ALARM = "Вы активировали Систему Тревоги, поэтому были вынуждены броситься в бегство."
    ACT_TRAP = "Вы попали в Ловушку, ваше действие было прервано"
    ACT_THEATRESTUFF = "Ваша новая роль – {}. Сыграйте ее достойно!"
    ACT_ANONYMOUSCALL_NO_SUSPECT = "Полиция проверила дом гражданина - {}. Достоверно, что он не является подозрительным."
    ACT_ANONYMOUSCALL_PLAYER = "Полиция проверила дом гражданина - {}. Достоверно, что он является Убийцей."
    ACT_ANONYMOUSCALL_SPY = "Полиция проверила дом гражданина - {}. Достоверно, что он является Шпионом."
    ACT_TAXES = "Соцработник покинул вас, доставив немало хлопот."
    ACT_ANTIDOTE = "Препарат нового поколения спас гражданина {} от неминуемой смерти"
    ACT_GANG = "Банда изрядно поколотила вас в эту ночь, не дав возможность осуществить задуманное."


class FinishTurn:
    ACT_FINISH_TURN = "Ваш ход завершен!"


class Errors:
    ACTION_CHOICE = "Ошибка! Введите номер доступного действия."
    CARD_CHOICE = "Ошибка! Введите номер доступной карты."
    TARGET = "Ошибка! Введите номер доступной цели."
    CARDS_ONE_TARGET = "Ошибка! Введите одну цель для выбранной карты."
    DATA_BASE_TARGETS = "Ошибка! Введите три цели для выбранной карты."
    DATA_BASE_SAME_TARGETS = "Ошибка! Все цели должны быть разными."
    TALES_TARGET = "Ошибка! Целью для карты Сплетни является номер ночи. Введите номер доступной ночи."
    CONFIRM_CHOICE = "Ошибка! Введите номер доступного действия."
