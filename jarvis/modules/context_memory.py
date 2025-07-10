from jarvis.interfaces.context import ContextEngineInterface

class MemoryContextEngine(ContextEngineInterface):
    def __init__(self):
        self._contexts = {}

    def store_context(self, user_id: str, context: dict) -> None:
        self._contexts[user_id] = context

    def retrieve_context(self, user_id: str) -> dict:
        return self._contexts.get(user_id, {})

    def clear_context(self, user_id: str) -> None:
        if user_id in self._contexts:
            del self._contexts[user_id]