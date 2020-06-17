from citizens.citizen import Citizen

from typing import List


def is_citizen_in_range(target_number: int, citizens: List[Citizen]) -> bool:
    return True


def validate_citizen_target_number(target_number: int, citizens: List[Citizen]) -> bool:
    return target_number is not None and is_citizen_in_range(target_number, citizens) and citizens[target_number].is_alive
