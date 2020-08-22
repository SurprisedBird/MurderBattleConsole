from effects.effect import Effect


class NoneEffect(Effect):
    def __init__(self, game: 'Game', name: str, creator: 'Citizen') -> None:
        # TODO: set correct priority
        super().__init__(game, name, creator, 0)

    def _activate_impl(self) -> bool:
        return True

    def _resolve_impl(self) -> bool:
        return True

    def _validate(self, target_number: int) -> bool:
        return True

    def _on_clear_impl(self) -> None:
        pass
