        Scenario: Data base effect implementation

Feature: Data base effect validation
                Given I get targets list
                Then I should see each target number should be in the range of citizens list
                And I should see 3 targets in the targets list
                And I should see only the target numbers are different
                Then validation method should return True

Feature: Data base effect activation
                Given activate method is called
                Then active player should get message "Выберите три цели, которые будут проанализированы с помощью базы данных..."
                And active player should enter the target number three times
                When validation is successful
                Then three targets should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Data base effect activated
                Given resolve method is called
                Then I should get relevant citizens types by targets
                When there are no Player or Spy among the citizens types
                Then player that activated Data base should get the message "База данных показала, что среди указанных граждан нет подозрительных личностей"
                When there are Player among the citizens types
                Then player that activated Data base should get the message "База данных показала, что среди указанных граждан есть Убийца"
                When there are Spy among the citizens types
                Then player that activated Data base should get the message "База данных показала, что среди указанных граждан есть Шпион"
                When there are Player and Spy among the citizens types
                Then player that activated Data base should get the message "База данных показала, что среди указанных граждан есть Убийца и Шпион"
                And method should return True