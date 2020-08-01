        Scenario: Taxes effect implementation

Feature: Taxes effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Taxes effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, которого сегодня посетит Соцработник..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Taxes effect resolve
                Given resolve method is called
                When the target is a Player
                And target player should get message "Этой ночью вас посетил жадный Соцработник. Выберите способ откупиться от него: 1. [Карта], 2. [HP]"
                When target player enter "1"
                Then the target player cards list should be shown and ordered by numbers
                And the target player should enter relevant card number to clear this card or enter 0 to change the initial choice
                When target player enter "2"
                Then the target player should lose 1 hp
                And target player should get message "Вы потеряли 1 HP"
                When the target is a Spy
                Then all players should get message "Ночь была неспокойной. [имя персонажа противника] оказался не тем за кого себя выдавал. Шпион, который скрывался под личиной [имя персонажа противника] в спешке покинул город."
                And Spy citizen should be removed from the citizens list
                When the target is a Citizen
                Then the target citizen card should be cleared
                When the resolve method is ended
                Then method should return True