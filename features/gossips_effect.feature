        Scenario: Gossips effect implementation

Feature: Gossips effect validation
                Given I get targets list
                Then I should see target number should be less or equal to the count of action_history dictionary length
                Then validation method should return True

Feature: Gossips effect activation
                Given activate method is called
                Then active player should get message "Выберите ночь, информация о которой будет предоставлена..."
                And active player should enter the round number
                When validation is successful
                Then round number should be set as effect round_story
                Then passive player should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Gossips effect resolve
                Given resolve method is called
                Then I should get relevant item from action_history dictionary
                And player that activated Gossips effect should get the message "Действие: [relevant_action_name], Цель: [relevant_action_target], Карта: [relevant_card_name], Цель: [relevant_card_target]"
                And method should return True