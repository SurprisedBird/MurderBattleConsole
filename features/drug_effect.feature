        Scenario: Drug effect implementation

Feature: Drug effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Drug effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, к дому которого будет отправлен Наркоман..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Drug effect resolve
                Given resolve method is called
                When Camera, Alarm, Trap, or Witness effect is in the target citizen effects list
                Then all Camera, Alarm, Trap, or Witness effects from the target citizen effects list should be change status to FINISHED
                And method should return True