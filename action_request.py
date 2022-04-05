from typing import Dict, List


class ActionRequest:
    def __init__(self) -> None:
        self.indexes: List[int] = []
        self.card_targets: List[int] = []

    def parsing(self, indexes):
        indexes = indexes.split(';')
        for i in range (0, 3):
            if indexes[i].isnumeric():
                self.indexes.append(int(indexes[i]))
            else:
                self.indexes.append(None)

        card_targets = indexes[3].split(',')

        for index in card_targets:
            if index.isnumeric():
                self.card_targets.append(int(index))
            else:
                self.card_targets.append(None)

    def clear_action_request(self):
        self.indexes = []
        self.card_targets = []


