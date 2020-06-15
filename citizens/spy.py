from citizens.citizen import Citizen


class Spy(Citizen):

    def __init__(self, name: str, hp: int = 1) -> None:
        # TODO: pass something except None
        Citizen.__init__(name, None, hp)
