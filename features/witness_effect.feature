        Scenario: Witness effect implementation

Feature: Witness effect validation
                Given I get targets list
                Then I should see the target number should be in the range of citizens list
                And I should see target is relevant to alive citizens
                Then validation method should return True

Feature: Witness effect activation
                Given activate method is called
                Then active player should get message "Выберите гражданина, на дом которого будет установлена Защита свидетеля..."
                And active player should enter the target number
                When validation is successful
                Then target should be appended into the effect targets list
                When validation is failed
                Then activation should be repeated

Feature: Witness effect resolve
                Given resolve method is called and effect life should be more than 0
                Then all players should get message "Городская полиция оцепила один из домов. Говорят, что они нашли ценного свидетеля по делу городских убийств."
                Then change decrease effect life on 1 and call return for resolve method
                Given resolve method is called and effect life should be 0
                When the player ativated witness is not active player
                And kill, steal or stage effect is on the target player
                Then player that activated kill, steal or stage effect should lose 1 hp
                Then player that activated kill, steal or stage effect should get message "Вы потеряли 1 HP"
                When the player ativated witness is active player
                Then target player should get message "1. [Продлить Защиту Свидетеля и потерять HP] 2. [Продлить Защиту Свидетеля и потерять Карту] 3. Сбросить Защиту Свидетеля"
                When target player enter "1" for extension
                Then the target player should lose 1 hp
                And target player should get message "Вы потеряли 1 HP"
                And resolve method should return False
                When target player enter "2" for card or hp choice
                Then the target player cards list should be shown and ordered by numbers
                And the target player should enter relevant card number to clear this card or enter 0 to change the initial choice
                And resolve method should return False
                When target player enter "3" for extension
                Then target player should get message "Защита Свидетеля была сброшена"
                And resolve method should return True