        Scenario: Anonymus call effect implementation

Feature: Anonymus call effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Anonymus call effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, которого сегодняшней ночью неизвестный обвинит с помощью анонимного звонка в полицию..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Anonymus call effect resolve
                Given resolve method is called
                Then all players should get message "В полицию поступил загадочный анонимный звонок, где высказывались обвинения в убийстве с указанием конкретного подозреваемого. Полиция решила перепроверить данную информацию"
                When the target is a Player
                Then the target player should lose 1 hp
                And target player should get message "Вы потеряли 1 HP"
                And active player should get message "Полиция проверила информацию. Подозреваемый оказался Убийцей!"
                When the target is a Spy
                Then active player should get message "Полиция проверила информацию. Подозреваемый оказался Шпионом!"
                When the target is a Citizen
                Then active player should get message "Полиция проверила информацию. Подозреваемый оказался невиновен!"
                And method should return True