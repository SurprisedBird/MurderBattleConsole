    Scenario: Night stage game flow implementation

Feature: Proceed game implementation
        Given the method proceed_game() is called
        Then all methods of the main phase should be called

Feature: Show night state
        Given the method show_night_state() is called
        Then I should see "Ваш ход" message
        And I should see "HP = [player current hp value]" message
        And I should see "Инсценировка [активна / отсутствует]" message
        And I should see "Личная карта: [player citizen_card]" message
        And I should see "Украденные карты: [player stolen_cards]" message
        And I should see the enumerated list of citizens by next pattern “n. citizen” where dead citizens marked by next pattern "n. citizen (мертв)"

Feature: Create action
        Given the method create_action() is called
        When availability actions are checked on the Player object relevant method
        Then I should see "Введите номер действия" message
        And I should see "0. [Ничего не делать] / 1. [Убийство] / 2. [Кража] / 3. [Инсценировка]" message if all actions are available
        When I print a number of action and press ENTER button
        Then new relevant Effect object should be created with an empty target

        Given the new action Effect with an empty target is created earlier
        Then I should see chosen effect activation message
        When activation is successful
        Then Effect object created earlier should be got relevant value for target variable
        And Effect object should be appended to the pre_actions list in ActionManager class

        Given the action Effect is created earlier and appended to the pre_actions list in ActionManager class
        When availability cards are checked on the Player object relevant method
        And the card can be chosen
        Then I should see "Введите номер карты" message
        When the card is not chosen
        Then new relevant NoCardEffect object should be created with an empty target
        When the card is chosen
        Then I should see the enumerated list where the first item is citizen_card of player and next items are stolen_cards of player
        When I print a number of card and press ENTER button
        Then new relevant Effect object should be created with an empty target

        Given the new card Effect with an empty target is created earlier
        Then I should see chosen effect activation message
        When activation is successful
        Then Effect object created earlier should be got relevant value for target variable
        And Effect object should be appended to the pre_actions list in ActionManager class

        Given action Effect and card Effect are successfully created and appended to the pre_actions list in ActionManager class
        Then I should see "[1. Подтвердить / 2. Отменить]" message
        When I choose "1" and press ENTER button
        Then pre_actions list is added to the actions_history dictionary in ActionManager class where round_number is a key
        Then pre_actions list is cleared
        When I choose "2" and press ENTER button
        Then pre_actions list is cleared
        And the create_action() method event should be repeated

Feature: Resolve effects
        Given the method resolve_effects() is called
        Then each citizen in the citizens list should be selected
        And each citizen effects list items should be ordered by priority from the biggest to the smallest number
        And each resolve() method should be called for each effect in the each citizen effects list
        And check_win() method should be called

Feature: Check win
        Given the method check_win() is called
        When active player hp more than 0 and passive player hp more than 0
        Then the method proceed_game() is called
        When active player hp is 0 and passive player hp is 0
        Then all players should get message "Убийцы нанесли друг другу смертельные раны и теперь город сможет спать спокойно. Ничья!"
        And the game should be finished
        When active player hp more than 0 and passive player hp is 0
        Then all players should get message "[имя активного игрока] настиг своего противника [имя пассивного игрока] и не оставил ему никаких шансов. Победа [имя активного игрока]!"
        And the game should be finished
        When active player hp is 0 and passive player hp more than 0
        Then all players should get message "[имя пассивного игрока] настиг своего противника [имя активного игрока] и не оставил ему никаких шансов. Победа [имя пассивного игрока]!"
        And the game should be finished