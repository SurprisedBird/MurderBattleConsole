from typing import Callable, List

import message_text_config as msg
import user_interaction


def read_target_number(message: str, validate_method: Callable[[int],
                                                               bool]) -> int:
    target_number = user_interaction.read_number(message)
    while (not validate_method(target_number)):
        user_interaction.show_active_instant(
            msg.CommonMessages.ERROR_INVALID_TARGET)
        target_number = user_interaction.read_number(message)

    return target_number


def save_message_for_player(game: 'Game', player: 'Citizen',
                            message: str) -> None:
    if player is game.active_player:
        user_interaction.save_active(message)
    elif player is game.passive_player:
        user_interaction.save_passive(message)
    else:
        # do nothing
        pass


# def save_message_for_oposite_player(game: 'Game', player: 'Citizen',
#                                     message: str) -> None:
#     if player is game.active_player:
#         user_interaction.save_passive(message)
#     elif player is game.passive_player:
#         user_interaction.save_active(message)
#     else:
#         # do nothing
#     pass


def is_action_effect(effect: 'Effect') -> bool:
    return type(effect).__name__ in [
        "KillEffect", "StealEffect", "StagingEffect"
    ]


def is_citizen_in_range(target_index: int, citizens: List['Citizen']) -> bool:
    return target_index >= 0 and target_index < len(citizens)


def validate_citizen_target_number(target_number: int,
                                   citizens: List['Citizen']) -> bool:
    return (target_number is not None
            and is_citizen_in_range(target_number - 1, citizens)
            and citizens[target_number - 1].is_alive)
