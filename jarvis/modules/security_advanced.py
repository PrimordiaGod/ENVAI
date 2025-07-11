from jarvis.interfaces.security import SecurityInterface
from typing import Dict, List, Optional, Any
import json
import datetime
import hashlib
import hmac
import base64
import jwt
import bcrypt
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AdvancedSecurity(SecurityInterface):
    def __init__(self):
        self._is_initialized = False
        self._encryption_key = None
        self._jwt_secret = None
        self._threat_patterns = []
        self._access_logs = []
        self._failed_attempts = {}
        self._session_tokens = {}
        self._biometric_data = {}

    def initialize(self, config: dict) -> bool:
        """Initialize advanced security system."""
        try:
            # Generate encryption key
            password = config.get('encryption_password', 'default_password').encode()
            salt = config.get('salt', b'default_salt')
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            self._encryption_key = key
            
            # Generate JWT secret
            self._jwt_secret = config.get('jwt_secret', 'default_jwt_secret')
            
            # Load threat patterns
            self._load_threat_patterns()
            
            self._is_initialized = True
            return True
        except Exception as e:
            print(f"Advanced security initialization failed: {e}")
            return False

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        if not self._is_initialized:
            return data
        
        try:
            f = Fernet(self._encryption_key)
            encrypted_data = f.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            print(f"Encryption failed: {e}")
            return data

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        if not self._is_initialized:
            return encrypted_data
        
        try:
            f = Fernet(self._encryption_key)
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = f.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            print(f"Decryption failed: {e}")
            return encrypted_data

    def hash_password(self, password: str) -> str:
        """Hash a password securely."""
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        password_bytes = password.encode('utf-8')
        stored_hash = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_hash)

    def generate_token(self, user_id: str, expires_in: int = 3600) -> str:
        """Generate a JWT token for user authentication."""
        if not self._is_initialized:
            return None
        
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
                'iat': datetime.datetime.utcnow(),
                'type': 'access'
            }
            token = jwt.encode(payload, self._jwt_secret, algorithm='HS256')
            return token
        except Exception as e:
            print(f"Token generation failed: {e}")
            return None

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode a JWT token."""
        if not self._is_initialized:
            return None
        
        try:
            payload = jwt.decode(token, self._jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None

    def detect_threats(self, data: dict) -> List[dict]:
        """Detect potential security threats."""
        if not self._is_initialized:
            return []
        
        threats = []
        
        # Check for SQL injection patterns
        sql_patterns = [
            r"(\b(union|select|insert|update|delete|drop|create|alter)\b)",
            r"(--|#|/\*|\*/)",
            r"(\b(and|or)\b\s+\d+\s*[=<>])"
        ]
        
        # Check for XSS patterns
        xss_patterns = [
            r"(<script[^>]*>.*?</script>)",
            r"(javascript:)",
            r"(on\w+\s*=)"
        ]
        
        # Check for command injection
        cmd_patterns = [
            r"(;|\||&|\$\(|\`)",
            r"(\b(cat|ls|rm|wget|curl|nc|telnet)\b)"
        ]
        
        # Convert data to string for pattern matching
        data_str = json.dumps(data)
        
        for pattern in sql_patterns + xss_patterns + cmd_patterns:
            matches = re.findall(pattern, data_str, re.IGNORECASE)
            if matches:
                threat_type = "sql_injection" if pattern in sql_patterns else \
                             "xss" if pattern in xss_patterns else "command_injection"
                
                threats.append({
                    'type': threat_type,
                    'pattern': pattern,
                    'matches': matches,
                    'severity': 'high',
                    'timestamp': datetime.datetime.now().isoformat()
                })
        
        return threats

    def log_access(self, user_id: str, action: str, success: bool, details: dict = None):
        """Log access attempts for security monitoring."""
        log_entry = {
            'user_id': user_id,
            'action': action,
            'success': success,
            'timestamp': datetime.datetime.now().isoformat(),
            'ip_address': details.get('ip_address', 'unknown'),
            'user_agent': details.get('user_agent', 'unknown'),
            'details': details or {}
        }
        
        self._access_logs.append(log_entry)
        
        # Keep only last 1000 logs
        if len(self._access_logs) > 1000:
            self._access_logs = self._access_logs[-1000:]

    def get_access_logs(self, user_id: str = None, limit: int = 100) -> List[dict]:
        """Get access logs for monitoring."""
        logs = self._access_logs
        
        if user_id:
            logs = [log for log in logs if log['user_id'] == user_id]
        
        return logs[-limit:] if limit else logs

    def check_rate_limit(self, user_id: str, action: str, max_attempts: int = 5, window: int = 300) -> bool:
        """Check if user has exceeded rate limits."""
        current_time = datetime.datetime.now()
        key = f"{user_id}:{action}"
        
        if key not in self._failed_attempts:
            self._failed_attempts[key] = []
        
        # Remove old attempts outside the window
        window_start = current_time - datetime.timedelta(seconds=window)
        self._failed_attempts[key] = [
            attempt for attempt in self._failed_attempts[key]
            if attempt > window_start
        ]
        
        # Check if limit exceeded
        if len(self._failed_attempts[key]) >= max_attempts:
            return False
        
        return True

    def record_failed_attempt(self, user_id: str, action: str):
        """Record a failed authentication attempt."""
        key = f"{user_id}:{action}"
        if key not in self._failed_attempts:
            self._failed_attempts[key] = []
        
        self._failed_attempts[key].append(datetime.datetime.now())

    def store_biometric_data(self, user_id: str, biometric_type: str, data: bytes) -> bool:
        """Store biometric data for authentication."""
        try:
            if user_id not in self._biometric_data:
                self._biometric_data[user_id] = {}
            
            # Hash the biometric data for storage
            hashed_data = hashlib.sha256(data).hexdigest()
            self._biometric_data[user_id][biometric_type] = hashed_data
            return True
        except Exception as e:
            print(f"Error storing biometric data: {e}")
            return False

    def verify_biometric_data(self, user_id: str, biometric_type: str, data: bytes) -> bool:
        """Verify biometric data against stored data."""
        try:
            if user_id not in self._biometric_data:
                return False
            
            if biometric_type not in self._biometric_data[user_id]:
                return False
            
            # Hash the provided data and compare
            hashed_data = hashlib.sha256(data).hexdigest()
            stored_hash = self._biometric_data[user_id][biometric_type]
            
            return hashed_data == stored_hash
        except Exception as e:
            print(f"Error verifying biometric data: {e}")
            return False

    def create_session(self, user_id: str, session_data: dict = None) -> str:
        """Create a new secure session."""
        session_id = hashlib.sha256(f"{user_id}:{datetime.datetime.now()}".encode()).hexdigest()
        
        session = {
            'user_id': user_id,
            'created': datetime.datetime.now().isoformat(),
            'last_activity': datetime.datetime.now().isoformat(),
            'data': session_data or {}
        }
        
        self._session_tokens[session_id] = session
        return session_id

    def validate_session(self, session_id: str) -> Optional[dict]:
        """Validate a session and return session data."""
        if session_id not in self._session_tokens:
            return None
        
        session = self._session_tokens[session_id]
        
        # Check if session is expired (24 hours)
        created_time = datetime.datetime.fromisoformat(session['created'])
        if datetime.datetime.now() - created_time > datetime.timedelta(hours=24):
            del self._session_tokens[session_id]
            return None
        
        # Update last activity
        session['last_activity'] = datetime.datetime.now().isoformat()
        return session

    def destroy_session(self, session_id: str) -> bool:
        """Destroy a session."""
        if session_id in self._session_tokens:
            del self._session_tokens[session_id]
            return True
        return False

    def _load_threat_patterns(self):
        """Load threat detection patterns."""
        self._threat_patterns = [
            # SQL Injection patterns
            r"(\b(union|select|insert|update|delete|drop|create|alter)\b)",
            r"(--|#|/\*|\*/)",
            r"(\b(and|or)\b\s+\d+\s*[=<>])",
            
            # XSS patterns
            r"(<script[^>]*>.*?</script>)",
            r"(javascript:)",
            r"(on\w+\s*=)",
            
            # Command injection patterns
            r"(;|\||&|\$\(|\`)",
            r"(\b(cat|ls|rm|wget|curl|nc|telnet)\b)",
            
            # Path traversal
            r"(\.\./|\.\.\\)",
            
            # LDAP injection
            r"(\*|\(|\)|\||&)",
            
            # NoSQL injection
            r"(\$where|\$ne|\$gt|\$lt)",
        ]

    def get_security_report(self) -> dict:
        """Generate a security report."""
        return {
            'total_access_logs': len(self._access_logs),
            'active_sessions': len(self._session_tokens),
            'failed_attempts': len(self._failed_attempts),
            'users_with_biometric': len(self._biometric_data),
            'recent_threats': len([log for log in self._access_logs[-100:] if not log['success']]),
            'system_status': 'secure' if self._is_initialized else 'insecure'
        }