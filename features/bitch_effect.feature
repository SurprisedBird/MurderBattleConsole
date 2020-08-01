        Scenario: Bitch effect implementation

Feature: Bitch effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Bitch effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, которого сегодня посетит Жрица Любви..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Bitch effect resolve
                Given resolve method is called and effect life should be more than 0
                Then kill, steal and stage effect shouldn't be available for target player
                And all players should get message "На охоту вышла Ночная Бабочка, готовая, следующей ночью, одарить одного из горожан своим визитом."
                Then target player should get message "Следующую ночь вы проведете с очаровательной красоткой и не сможете совершать действие убийства, кражи или инсценировки."
                And change effect life to 0
                And method should be return False
                Given resolve method is called and effect life should be 0
                Then method should return True

Feature: Bitch effect cleaning
                Then kill, steal and stage effect should be available for target player