from user_interactions.base_user_interaction import (BaseUserInteraction,
                                                     MessageScope)


class UserInteraction(BaseUserInteraction):
    def __init__(self, context: 'Context'):
        super().__init__(context)

    def show_global_instant(self, text: str) -> None:
        print(f"{MessageScope.GLOBAL.name}: {text}")

    def show_active_instant(self, text: str) -> None:
        print(self.users[0])
        print(f"{MessageScope.ACTIVE.name}: {text}")

    def show_passive_instant(self, text: str) -> None:
        print(self.users[1])
        print(f"{MessageScope.PASSIVE.name}: {text}")

    def show_all(self) -> None:
        for scope, text_list in self._prepared_messages.items():
            print(f"{scope.name}:")
            for text in text_list:
                print(f"\t{text}")

        self._clear_messages()
