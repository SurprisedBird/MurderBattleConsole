        Scenario: Trap effect implementation

Feature: Trap effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Trap effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, на дом которого будет установлена Ловушка..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Trap effect resolve
                Given resolve method is called and effect life should be more than 0
                When kill, steal or stage effect is on the target citizen
                Then all players should get message "В дом [имя целевого гражданина] вломился неизвестный, но оказался в западне."
                And player that activated kill, steal or stage effect should lose 1 HP
                And kill, steal or stage effect should be cleared
                And player that activated kill, steal or stage effect should get message "Вы потеряли 1 HP"
                When the resolve method is ended
                Then resolve method should return False
                Then change effect life to 0 and call return for resolve method
                Given resolve method is called and effect life should be 0
                Then resolve method should return True