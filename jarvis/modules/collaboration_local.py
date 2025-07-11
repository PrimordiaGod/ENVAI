from jarvis.interfaces.collaboration import CollaborationInterface, RealTimeInterface, UserManagementInterface
from typing import Dict, List, Optional, Any, Callable
import json
import datetime
import threading
import time
import uuid
import bcrypt

class LocalCollaboration(CollaborationInterface, RealTimeInterface, UserManagementInterface):
    def __init__(self):
        self._is_initialized = False
        self._workspaces = {}
        self._sessions = {}
        self._users = {}
        self._shared_contexts = {}
        self._session_messages = {}
        self._message_callback = None

    def initialize(self, config: dict) -> bool:
        """Initialize local collaboration system."""
        try:
            # Create some default users for testing
            self._create_default_users()
            self._is_initialized = True
            return True
        except Exception as e:
            print(f"Collaboration initialization failed: {e}")
            return False

    # Collaboration Interface Methods
    def create_workspace(self, name: str, owner_id: str) -> str:
        """Create a new collaborative workspace."""
        try:
            workspace_id = str(uuid.uuid4())
            workspace = {
                'id': workspace_id,
                'name': name,
                'owner_id': owner_id,
                'members': [owner_id],
                'created': datetime.datetime.now().isoformat(),
                'shared_context': {}
            }
            
            self._workspaces[workspace_id] = workspace
            return workspace_id
        except Exception as e:
            print(f"Error creating workspace: {e}")
            return None

    def join_workspace(self, workspace_id: str, user_id: str) -> bool:
        """Join an existing workspace."""
        if workspace_id not in self._workspaces:
            return False
        
        if user_id not in self._workspaces[workspace_id]['members']:
            self._workspaces[workspace_id]['members'].append(user_id)
            return True
        
        return True

    def leave_workspace(self, workspace_id: str, user_id: str) -> bool:
        """Leave a workspace."""
        if workspace_id not in self._workspaces:
            return False
        
        if user_id in self._workspaces[workspace_id]['members']:
            self._workspaces[workspace_id]['members'].remove(user_id)
            return True
        
        return False

    def get_workspace_members(self, workspace_id: str) -> List[dict]:
        """Get list of workspace members."""
        if workspace_id not in self._workspaces:
            return []
        
        members = []
        for user_id in self._workspaces[workspace_id]['members']:
            user_info = self.get_user(user_id)
            if user_info:
                members.append(user_info)
        
        return members

    def share_context(self, workspace_id: str, context: dict) -> bool:
        """Share context with workspace members."""
        if workspace_id not in self._workspaces:
            return False
        
        self._workspaces[workspace_id]['shared_context'] = context
        return True

    def get_shared_context(self, workspace_id: str) -> dict:
        """Get shared context for a workspace."""
        if workspace_id not in self._workspaces:
            return {}
        
        return self._workspaces[workspace_id].get('shared_context', {})

    # Real-Time Interface Methods
    def start_session(self, session_id: str, participants: List[str]) -> bool:
        """Start a real-time session."""
        try:
            session = {
                'id': session_id,
                'participants': participants,
                'started': datetime.datetime.now().isoformat(),
                'active': True
            }
            
            self._sessions[session_id] = session
            self._session_messages[session_id] = []
            return True
        except Exception as e:
            print(f"Error starting session: {e}")
            return False

    def end_session(self, session_id: str) -> bool:
        """End a real-time session."""
        if session_id in self._sessions:
            self._sessions[session_id]['active'] = False
            return True
        return False

    def send_message(self, session_id: str, user_id: str, message: str) -> bool:
        """Send a message in a real-time session."""
        if session_id not in self._sessions or not self._sessions[session_id]['active']:
            return False
        
        message_data = {
            'id': str(uuid.uuid4()),
            'session_id': session_id,
            'user_id': user_id,
            'message': message,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self._session_messages[session_id].append(message_data)
        
        # Trigger callback if set
        if self._message_callback:
            self._message_callback(session_id, user_id, message)
        
        return True

    def get_session_messages(self, session_id: str) -> List[dict]:
        """Get messages from a session."""
        return self._session_messages.get(session_id, [])

    def set_message_callback(self, callback: Callable[[str, str, str], None]) -> None:
        """Set callback for incoming messages."""
        self._message_callback = callback

    # User Management Interface Methods
    def create_user(self, user_info: dict) -> str:
        """Create a new user."""
        try:
            user_id = str(uuid.uuid4())
            
            # Hash password if provided
            if 'password' in user_info:
                password = user_info['password'].encode('utf-8')
                hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                user_info['password_hash'] = hashed.decode('utf-8')
                del user_info['password']
            
            user_info['id'] = user_id
            user_info['created'] = datetime.datetime.now().isoformat()
            
            self._users[user_id] = user_info
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def get_user(self, user_id: str) -> dict:
        """Get user information."""
        if user_id in self._users:
            user_info = self._users[user_id].copy()
            # Remove sensitive information
            if 'password_hash' in user_info:
                del user_info['password_hash']
            return user_info
        return None

    def update_user(self, user_id: str, updates: dict) -> bool:
        """Update user information."""
        if user_id not in self._users:
            return False
        
        # Hash password if provided
        if 'password' in updates:
            password = updates['password'].encode('utf-8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            updates['password_hash'] = hashed.decode('utf-8')
            del updates['password']
        
        self._users[user_id].update(updates)
        return True

    def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def list_users(self) -> List[dict]:
        """List all users."""
        users = []
        for user_id, user_info in self._users.items():
            user_data = user_info.copy()
            if 'password_hash' in user_data:
                del user_data['password_hash']
            users.append(user_data)
        return users

    def authenticate_user(self, credentials: dict) -> Optional[str]:
        """Authenticate a user and return user ID."""
        username = credentials.get('username')
        password = credentials.get('password')
        
        if not username or not password:
            return None
        
        # Find user by username
        for user_id, user_info in self._users.items():
            if user_info.get('username') == username:
                # Check password
                if 'password_hash' in user_info:
                    password_bytes = password.encode('utf-8')
                    stored_hash = user_info['password_hash'].encode('utf-8')
                    if bcrypt.checkpw(password_bytes, stored_hash):
                        return user_id
        
        return None

    def _create_default_users(self):
        """Create default users for testing."""
        default_users = [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'name': 'Alice Johnson',
                'role': 'admin'
            },
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'name': 'Bob Smith',
                'role': 'user'
            },
            {
                'username': 'charlie',
                'email': 'charlie@example.com',
                'name': 'Charlie Brown',
                'role': 'user'
            }
        ]
        
        for user_info in default_users:
            user_info['password'] = 'password123'  # Default password
            self.create_user(user_info)

    def get_workspace_info(self, workspace_id: str) -> dict:
        """Get workspace information."""
        if workspace_id not in self._workspaces:
            return {}
        
        workspace = self._workspaces[workspace_id].copy()
        workspace['member_count'] = len(workspace['members'])
        return workspace

    def list_workspaces(self) -> List[dict]:
        """List all workspaces."""
        workspaces = []
        for workspace_id, workspace in self._workspaces.items():
            workspace_info = workspace.copy()
            workspace_info['member_count'] = len(workspace['members'])
            workspaces.append(workspace_info)
        return workspaces

    def list_sessions(self) -> List[dict]:
        """List all active sessions."""
        sessions = []
        for session_id, session in self._sessions.items():
            if session['active']:
                session_info = session.copy()
                session_info['message_count'] = len(self._session_messages.get(session_id, []))
                sessions.append(session_info)
        return sessions