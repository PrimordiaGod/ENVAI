from abc import ABC, abstractmethod

class SelfModificationInterface(ABC):
    @abstractmethod
    def propose_change(self, diff: str) -> bool:
        """Propose a code change. Returns True if accepted."""
        pass

    @abstractmethod
    def apply_change(self, diff: str) -> bool:
        """Apply a code change. Returns True if successful."""
        pass

    @abstractmethod
    def rollback(self) -> bool:
        """Rollback to the previous stable version. Returns True if successful."""
        pass

    @abstractmethod
    def log_change(self, diff: str) -> None:
        """Log a code change for auditing purposes."""
        pass