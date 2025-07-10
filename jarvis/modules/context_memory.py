from jarvis.interfaces.context import ContextEngineInterface
from typing import Dict, List, Optional, Any
import json
import datetime
from collections import defaultdict

class MemoryContextEngine(ContextEngineInterface):
    def __init__(self):
        self._contexts = {}  # Short-term context
        self._long_term_memories = {}  # Long-term memory
        self._user_preferences = {}  # User preferences
        self._conversation_history = defaultdict(list)  # Conversation patterns
        self._intent_patterns = defaultdict(list)  # Intent analysis

    def store_context(self, user_id: str, context: dict) -> None:
        self._contexts[user_id] = context

    def retrieve_context(self, user_id: str) -> dict:
        return self._contexts.get(user_id, {})

    def clear_context(self, user_id: str) -> None:
        if user_id in self._contexts:
            del self._contexts[user_id]

    def store_long_term_memory(self, user_id: str, memory: dict) -> None:
        """Store long-term memory with timestamp and categorization."""
        if user_id not in self._long_term_memories:
            self._long_term_memories[user_id] = []
        
        memory_entry = {
            'data': memory,
            'timestamp': datetime.datetime.now().isoformat(),
            'category': memory.get('category', 'general')
        }
        self._long_term_memories[user_id].append(memory_entry)

    def retrieve_long_term_memory(self, user_id: str) -> dict:
        """Retrieve all long-term memories for a user."""
        memories = self._long_term_memories.get(user_id, [])
        return {
            'memories': memories,
            'count': len(memories),
            'categories': list(set(m.get('category', 'general') for m in memories))
        }

    def anticipate_user_intent(self, user_id: str, current_input: str) -> List[str]:
        """Anticipate user's next likely actions based on patterns."""
        # Simple pattern matching for Phase 2
        # In future phases, this could use ML models
        patterns = self._intent_patterns.get(user_id, [])
        current_pattern = self._extract_pattern(current_input)
        
        # Store current pattern
        patterns.append({
            'input': current_input,
            'pattern': current_pattern,
            'timestamp': datetime.datetime.now().isoformat()
        })
        self._intent_patterns[user_id] = patterns[-10:]  # Keep last 10 patterns
        
        # Simple anticipation based on common patterns
        anticipations = []
        if 'research' in current_input.lower() or 'search' in current_input.lower():
            anticipations.append("Would you like me to search for more specific information?")
        if 'weather' in current_input.lower():
            anticipations.append("Would you like me to check the weather forecast?")
        if 'schedule' in current_input.lower() or 'calendar' in current_input.lower():
            anticipations.append("Would you like me to help with scheduling?")
        
        return anticipations

    def update_user_preferences(self, user_id: str, preferences: dict) -> None:
        """Update user preferences with new data."""
        if user_id not in self._user_preferences:
            self._user_preferences[user_id] = {}
        
        # Merge new preferences with existing ones
        self._user_preferences[user_id].update(preferences)

    def get_user_preferences(self, user_id: str) -> dict:
        """Get user preferences for personalization."""
        return self._user_preferences.get(user_id, {})

    def analyze_conversation_patterns(self, user_id: str) -> dict:
        """Analyze conversation patterns to improve anticipation."""
        history = self._conversation_history.get(user_id, [])
        
        if not history:
            return {'patterns': [], 'topics': [], 'frequency': {}}
        
        # Analyze patterns
        topics = defaultdict(int)
        time_patterns = defaultdict(int)
        
        for entry in history[-50:]:  # Analyze last 50 conversations
            topics[entry.get('topic', 'general')] += 1
            hour = datetime.datetime.fromisoformat(entry['timestamp']).hour
            time_patterns[hour] += 1
        
        return {
            'patterns': list(topics.items()),
            'topics': list(topics.keys()),
            'frequency': dict(topics),
            'time_patterns': dict(time_patterns),
            'total_conversations': len(history)
        }

    def _extract_pattern(self, text: str) -> str:
        """Extract a simple pattern from text input."""
        # Simple pattern extraction for Phase 2
        # In future phases, this could use NLP
        words = text.lower().split()
        if len(words) < 2:
            return text.lower()
        
        # Extract key words (simple approach)
        key_words = [w for w in words if len(w) > 3]
        return ' '.join(key_words[:3])  # Return up to 3 key words

    def add_conversation_entry(self, user_id: str, input_text: str, response: str, topic: str = 'general'):
        """Add a conversation entry for pattern analysis."""
        entry = {
            'input': input_text,
            'response': response,
            'topic': topic,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self._conversation_history[user_id].append(entry)