        Scenario: Camera effect implementation

Feature: Camera effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Camera effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, на дом которого будет установлена Видеокамера..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Camera effect resolve
                Given resolve method is called
                When kill, steal or stage effect is on the target citizen
                Then player that activated Camera should get message "Видеокамера зафиксировала как [роль игрока, который осуществил Убийство или Кражу] вломился в дом [целевой гражданин]Видеокамера зафиксировала как [роль игрока, который осуществил Убийство или Кражу] вломился в дом [целевой гражданин]"
                And method should return True