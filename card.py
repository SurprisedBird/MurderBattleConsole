from effect import Effect

class Card:

    def __init__(self, name : str, effect : Effect) -> None:
        self._name = name
        self._effect = effect

    