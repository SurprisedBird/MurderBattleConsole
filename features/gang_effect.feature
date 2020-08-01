        Scenario: Gang effect implementation

Feature: Gang effect validation
                Given I get targets list
                Then validation method should return True

Feature: Gang effect activation
                Given activate method is called
                Then active player should get message "Банда вышла на охоту и следующий ход никто не посмеет помешать вашим планам."

Feature: Gang effect resolve
                Given resolve method is called and effect life should be more than 0
                When any card effect is on the target citizen effects list and activation_round more than gang activation_round
                Then player that activated any effect with activation_round more than gang activation_round should get message "Банда изрядно поколотила вас в эту ночь, не дав возможность осуществить задуманное."
                And effect with activation_round more than gang activation_round should be cleared
                And method should return True