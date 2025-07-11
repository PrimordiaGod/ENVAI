from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable

class CollaborationInterface(ABC):
    @abstractmethod
    def initialize(self, config: dict) -> bool:
        """Initialize collaboration system."""
        pass

    @abstractmethod
    def create_workspace(self, name: str, owner_id: str) -> str:
        """Create a new collaborative workspace."""
        pass

    @abstractmethod
    def join_workspace(self, workspace_id: str, user_id: str) -> bool:
        """Join an existing workspace."""
        pass

    @abstractmethod
    def leave_workspace(self, workspace_id: str, user_id: str) -> bool:
        """Leave a workspace."""
        pass

    @abstractmethod
    def get_workspace_members(self, workspace_id: str) -> List[dict]:
        """Get list of workspace members."""
        pass

    @abstractmethod
    def share_context(self, workspace_id: str, context: dict) -> bool:
        """Share context with workspace members."""
        pass

    @abstractmethod
    def get_shared_context(self, workspace_id: str) -> dict:
        """Get shared context for a workspace."""
        pass

class RealTimeInterface(ABC):
    @abstractmethod
    def start_session(self, session_id: str, participants: List[str]) -> bool:
        """Start a real-time session."""
        pass

    @abstractmethod
    def end_session(self, session_id: str) -> bool:
        """End a real-time session."""
        pass

    @abstractmethod
    def send_message(self, session_id: str, user_id: str, message: str) -> bool:
        """Send a message in a real-time session."""
        pass

    @abstractmethod
    def get_session_messages(self, session_id: str) -> List[dict]:
        """Get messages from a session."""
        pass

    @abstractmethod
    def set_message_callback(self, callback: Callable[[str, str, str], None]) -> None:
        """Set callback for incoming messages."""
        pass

class UserManagementInterface(ABC):
    @abstractmethod
    def create_user(self, user_info: dict) -> str:
        """Create a new user."""
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> dict:
        """Get user information."""
        pass

    @abstractmethod
    def update_user(self, user_id: str, updates: dict) -> bool:
        """Update user information."""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        pass

    @abstractmethod
    def list_users(self) -> List[dict]:
        """List all users."""
        pass

    @abstractmethod
    def authenticate_user(self, credentials: dict) -> Optional[str]:
        """Authenticate a user and return user ID."""
        pass