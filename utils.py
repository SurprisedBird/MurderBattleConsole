from typing import List

from citizens.citizen import Citizen


def is_citizen_in_range(target_index: int, citizens: List[Citizen]) -> bool:
    return target_index >= 0 and target_index < len(citizens)


def validate_citizen_target_number(target_number: int,
                                   citizens: List[Citizen]) -> bool:
    return (target_number is not None
            and is_citizen_in_range(target_number - 1, citizens)
            and citizens[target_number - 1].is_alive)
