from citizens.citizen import Citizen

from typing import List


def is_citizen_in_range(target_number: int, citizens: List[Citizen]) -> bool:
    return True


def validate_citizen_target_number(target_number: int, citizens: List[Citizen]) -> bool:
    return target_number is not None and is_citizen_in_range(target_number-1, citizens) and citizens[target_number-1].is_alive


def find_citizen_index(citizens, creator, target):
    creator_index = [index for index, citizen in enumerate(
        citizens) if citizen is creator][0]
    target_index = [index for index, citizen in enumerate(
        citizens) if citizen is target][0]

    return creator_index, target_index
