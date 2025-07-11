from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable

class CloudStorageInterface(ABC):
    @abstractmethod
    def initialize(self, config: dict) -> bool:
        """Initialize cloud storage connection."""
        pass

    @abstractmethod
    def upload_data(self, key: str, data: bytes, metadata: dict = None) -> bool:
        """Upload data to cloud storage."""
        pass

    @abstractmethod
    def download_data(self, key: str) -> Optional[bytes]:
        """Download data from cloud storage."""
        pass

    @abstractmethod
    def delete_data(self, key: str) -> bool:
        """Delete data from cloud storage."""
        pass

    @abstractmethod
    def list_data(self, prefix: str = "") -> List[dict]:
        """List available data in cloud storage."""
        pass

    @abstractmethod
    def sync_to_cloud(self, local_data: dict) -> bool:
        """Sync local data to cloud storage."""
        pass

    @abstractmethod
    def sync_from_cloud(self) -> dict:
        """Sync data from cloud storage to local."""
        pass

    @abstractmethod
    def get_sync_status(self) -> dict:
        """Get synchronization status."""
        pass

    @abstractmethod
    def set_sync_callback(self, callback: Callable[[str, dict], None]) -> None:
        """Set callback for sync events."""
        pass

    @abstractmethod
    def encrypt_before_upload(self, data: bytes) -> bytes:
        """Encrypt data before uploading to cloud."""
        pass

    @abstractmethod
    def decrypt_after_download(self, data: bytes) -> bytes:
        """Decrypt data after downloading from cloud."""
        pass