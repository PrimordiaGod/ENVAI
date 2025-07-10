from abc import ABC, abstractmethod

class SecureStorageInterface(ABC):
    @abstractmethod
    def store_data(self, key: str, data: bytes) -> None:
        """Store encrypted data by key."""
        pass

    @abstractmethod
    def retrieve_data(self, key: str) -> bytes:
        """Retrieve encrypted data by key."""
        pass

    @abstractmethod
    def delete_data(self, key: str) -> None:
        """Delete data by key."""
        pass