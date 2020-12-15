from citizens.citizen import Citizen


class Spy(Citizen):
    def __init__(self, context: 'Context', name: str, hp: int = 1) -> None:
        # TODO: pass something except None
        super().__init__(context, name, None, hp)
