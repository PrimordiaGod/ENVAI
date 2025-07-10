from abc import ABC, abstractmethod

class UserInteractionInterface(ABC):
    @abstractmethod
    def send_message(self, message: str) -> str:
        """Send a message to the user and return the assistant's response."""
        pass

    @abstractmethod
    def get_user_input(self) -> str:
        """Retrieve input from the user."""
        pass