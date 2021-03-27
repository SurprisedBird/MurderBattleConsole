from typing import Callable, List, Tuple

import message_text_config as msg
from effects.effect import InputStatusCode
from user_interactions.user_interaction import UserInteraction


def read_target_number(context: 'Context', message: str,
                       validate_method: InputStatusCode) -> int:
    target_number = context.user_interaction.read_number(message)

    input_status_code = validate_method(target_number)
    while (input_status_code is not InputStatusCode.OK):
        context.user_interaction.show_active_instant(input_status_code.value)
        target_number = context.user_interaction.read_number(message)
        input_status_code = validate_method(target_number)

    return target_number


def save_message_for_player(context: 'Context', player: 'Citizen',
                            message: str) -> None:
    if player is context.city.active_player:
        context.user_interaction.save_active(message)
    elif player is context.city.passive_player:
        context.user_interaction.save_passive(message)
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
        'KillEffect', 'StealEffect', 'StagingEffect'
    ]


def is_citizen_in_range(target_index: int, citizens: List['Citizen']) -> bool:
    return target_index >= 0 and target_index < len(citizens)


def validate_citizen_target_number(
        target_number: int,
        citizens: List['Citizen'],
        self_as_target_allowed: bool = True,
        creator: 'Citizen' = None) -> InputStatusCode:
    is_valid = (target_number is not None
                and is_citizen_in_range(target_number - 1, citizens)
                and citizens[target_number - 1].is_alive)

    is_self_as_target = \
        (citizens[target_number - 1] is creator) \
        if is_valid else False

    if not self_as_target_allowed and is_self_as_target:
        return InputStatusCode.NOK_SELF_AS_TARGET
    elif not is_valid:
        return InputStatusCode.NOK_INVALID_TARGET

    return InputStatusCode.OK


def is_player(citizen: 'Citizen') -> bool:
    return type(citizen).__name__ == 'Player'


def is_spy(citizen: 'Citizen') -> bool:
    return type(citizen).__name__ == 'Spy'


def contains_player(citizens: List['Citizen']) -> bool:
    roles = [type(target).__name__ for target in citizens]
    return 'Player' in roles


def contains_spy(citizens: List['Citizen']) -> bool:
    roles = [type(target).__name__ for target in citizens]
    return 'Spy' in roles
