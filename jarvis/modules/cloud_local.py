from jarvis.interfaces.cloud import CloudStorageInterface
from typing import Dict, List, Optional, Any, Callable
import os
import json
import datetime
from cryptography.fernet import Fernet

class LocalCloudStorage(CloudStorageInterface):
    def __init__(self):
        self._is_initialized = False
        self._cloud_directory = "cloud_storage"
        self._sync_callback = None
        self._encryption_key = None
        self._sync_status = {
            'last_sync': None,
            'sync_count': 0,
            'errors': []
        }

    def initialize(self, config: dict) -> bool:
        """Initialize local cloud storage simulation."""
        try:
            # Create cloud storage directory
            if not os.path.exists(self._cloud_directory):
                os.makedirs(self._cloud_directory)
            
            # Initialize encryption
            key_file = os.path.join(self._cloud_directory, "cloud.key")
            if not os.path.exists(key_file):
                self._encryption_key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(self._encryption_key)
            else:
                with open(key_file, 'rb') as f:
                    self._encryption_key = f.read()
            
            self._is_initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize cloud storage: {e}")
            return False

    def upload_data(self, key: str, data: bytes, metadata: dict = None) -> bool:
        """Upload data to local cloud storage."""
        if not self._is_initialized:
            return False
        
        try:
            # Encrypt data before storage
            encrypted_data = self.encrypt_before_upload(data)
            
            # Store encrypted data
            file_path = os.path.join(self._cloud_directory, f"{key}.enc")
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Store metadata
            if metadata:
                meta_path = os.path.join(self._cloud_directory, f"{key}.meta")
                with open(meta_path, 'w') as f:
                    json.dump(metadata, f)
            
            return True
        except Exception as e:
            print(f"Error uploading data: {e}")
            return False

    def download_data(self, key: str) -> Optional[bytes]:
        """Download data from local cloud storage."""
        if not self._is_initialized:
            return None
        
        try:
            file_path = os.path.join(self._cloud_directory, f"{key}.enc")
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            decrypted_data = self.decrypt_after_download(encrypted_data)
            return decrypted_data
        except Exception as e:
            print(f"Error downloading data: {e}")
            return None

    def delete_data(self, key: str) -> bool:
        """Delete data from local cloud storage."""
        try:
            file_path = os.path.join(self._cloud_directory, f"{key}.enc")
            meta_path = os.path.join(self._cloud_directory, f"{key}.meta")
            
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(meta_path):
                os.remove(meta_path)
            
            return True
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False

    def list_data(self, prefix: str = "") -> List[dict]:
        """List available data in local cloud storage."""
        if not self._is_initialized:
            return []
        
        data_list = []
        try:
            for filename in os.listdir(self._cloud_directory):
                if filename.endswith('.enc') and filename.startswith(prefix):
                    key = filename[:-4]  # Remove .enc extension
                    file_path = os.path.join(self._cloud_directory, filename)
                    meta_path = os.path.join(self._cloud_directory, f"{key}.meta")
                    
                    file_info = {
                        'key': key,
                        'size': os.path.getsize(file_path),
                        'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    }
                    
                    # Add metadata if available
                    if os.path.exists(meta_path):
                        try:
                            with open(meta_path, 'r') as f:
                                file_info['metadata'] = json.load(f)
                        except:
                            pass
                    
                    data_list.append(file_info)
        except Exception as e:
            print(f"Error listing data: {e}")
        
        return data_list

    def sync_to_cloud(self, local_data: dict) -> bool:
        """Sync local data to cloud storage."""
        if not self._is_initialized:
            return False
        
        try:
            sync_count = 0
            for key, data in local_data.items():
                if isinstance(data, str):
                    data_bytes = data.encode('utf-8')
                elif isinstance(data, dict):
                    data_bytes = json.dumps(data).encode('utf-8')
                else:
                    data_bytes = bytes(data)
                
                if self.upload_data(key, data_bytes):
                    sync_count += 1
            
            self._sync_status['last_sync'] = datetime.datetime.now().isoformat()
            self._sync_status['sync_count'] += sync_count
            
            if self._sync_callback:
                self._sync_callback('upload', {'count': sync_count})
            
            return True
        except Exception as e:
            self._sync_status['errors'].append(str(e))
            return False

    def sync_from_cloud(self) -> dict:
        """Sync data from cloud storage to local."""
        if not self._is_initialized:
            return {}
        
        try:
            cloud_data = {}
            data_list = self.list_data()
            
            for item in data_list:
                key = item['key']
                data = self.download_data(key)
                if data:
                    try:
                        # Try to decode as JSON first
                        cloud_data[key] = json.loads(data.decode('utf-8'))
                    except:
                        # Fall back to string
                        cloud_data[key] = data.decode('utf-8')
            
            self._sync_status['last_sync'] = datetime.datetime.now().isoformat()
            
            if self._sync_callback:
                self._sync_callback('download', {'count': len(cloud_data)})
            
            return cloud_data
        except Exception as e:
            self._sync_status['errors'].append(str(e))
            return {}

    def get_sync_status(self) -> dict:
        """Get synchronization status."""
        return self._sync_status.copy()

    def set_sync_callback(self, callback: Callable[[str, dict], None]) -> None:
        """Set callback for sync events."""
        self._sync_callback = callback

    def encrypt_before_upload(self, data: bytes) -> bytes:
        """Encrypt data before uploading to cloud."""
        if not self._encryption_key:
            return data
        
        fernet = Fernet(self._encryption_key)
        return fernet.encrypt(data)

    def decrypt_after_download(self, data: bytes) -> bytes:
        """Decrypt data after downloading from cloud."""
        if not self._encryption_key:
            return data
        
        fernet = Fernet(self._encryption_key)
        return fernet.decrypt(data)