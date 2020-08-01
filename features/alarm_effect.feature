        Scenario: Alarm effect implementation

Feature: Alarm effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Alarm effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, на дом которого будет установлена Система Тревоги..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Alarm effect resolve
                Given resolve method is called
                When kill, steal or stage effects is on the target
                Then kill, steal or stage effect should be removed from target
                And player that activated Alarm effect should get message "Система тревоги была активирована."
                And active player should get message "Вы активировали Систему Тревоги, поэтому были вынуждены броситься в бегство."
                And method should return True