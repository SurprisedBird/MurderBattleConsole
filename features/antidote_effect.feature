        Scenario: Antidote effect implementation

Feature: Antidote effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Antidote effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, который следующий ход будет защищен от смертельной атаки..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Antidote effect resolve
                Given resolve method is called and effect life should be more than 0
                When the resolve method is ended
                Then change effect life to 0 and call return for resolve method
                Given resolve method is called and effect life should be 0
                And method should return True