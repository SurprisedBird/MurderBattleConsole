from typing import List


class Citizen:
    def __init__(self,
                 context: 'Context',
                 name: str,
                 citizen_card: 'Card',
                 hp: int = 1) -> None:
        self.context = context
        self.name = name
        self.hp = hp
        self.citizen_card = citizen_card
        self.effects: List['Effect'] = []

    @property
    def is_alive(self) -> bool:
        return self.hp > 0
