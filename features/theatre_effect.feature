        Scenario: Theatre effect implementation

Feature: Theatre effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Theatre effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, роль которого будет теперь отображаться вместо вашей при анализе с помощью эффектов обнаружения..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Theatre effect resolve
                Given resolve method is called
                Then active player should get message "Ваша новая роль – [роль целевого гражданина]. Сыграйте ее достойно!"
                Then method should return True