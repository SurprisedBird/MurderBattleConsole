from effects.effect import Effect, InputStatusCode


class NoneEffect(Effect):
    def __init__(self, context: 'Context', name: str,
                 creator: 'Citizen') -> None:
        # TODO: set correct priority
        super().__init__(context, name, creator)

    def _activate_impl(self) -> bool:
        return True

    def _resolve_impl(self) -> bool:
        return True

    def _validate(self, target_number: int) -> InputStatusCode:
        return InputStatusCode.OK

    def _on_clear_impl(self) -> None:
        pass
