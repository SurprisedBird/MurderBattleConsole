from typing import Dict, List


class ActionManager:
    def __init__(self) -> None:
        self.pre_actions: List['Effect'] = []
        self.actions_history: Dict[int, 'Effect'] = {}

    def clear_pre_actions(self) -> None:
        self.pre_actions = []

    def add_pre_action(self, action: 'Effect'):
        self.pre_actions.append(action)

    def store_actions_history(self, round_number: int):
        self.actions_history[round_number] = self.pre_actions
        self.pre_actions = []
