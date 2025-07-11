from jarvis.interfaces.ai_model import AIModelInterface, AIModelResponse
from typing import Dict, List, Optional, Any
import time
import json
import re
from datetime import datetime

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI library not available. Install with: pip install openai")

class OpenAIInterface(AIModelInterface):
    """OpenAI GPT integration for enhanced AI capabilities."""
    
    def __init__(self):
        self._client = None
        self._current_model = "gpt-3.5-turbo"
        self._api_key = None
        self._is_initialized = False
        self._usage_stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'last_request': None
        }
        self._available_models = [
            {'name': 'gpt-3.5-turbo', 'max_tokens': 4096, 'cost_per_1k': 0.002},
            {'name': 'gpt-4', 'max_tokens': 8192, 'cost_per_1k': 0.03},
            {'name': 'gpt-4-turbo', 'max_tokens': 128000, 'cost_per_1k': 0.01}
        ]

    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize OpenAI client with configuration."""
        if not OPENAI_AVAILABLE:
            print("OpenAI library not available. Using simulation mode.")
            self._is_initialized = True
            return True

        try:
            api_key = config.get('api_key')
            if not api_key:
                print("❌ OpenAI API key not provided")
                return False

            self._api_key = api_key
            self._client = openai.OpenAI(api_key=api_key)
            
            # Test the connection
            response = self._client.models.list()
            if response:
                self._is_initialized = True
                print("✅ OpenAI interface initialized successfully")
                return True
            else:
                print("❌ Failed to connect to OpenAI API")
                return False

        except Exception as e:
            print(f"❌ OpenAI initialization failed: {e}")
            return False

    def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AIModelResponse:
        """Generate a response using OpenAI GPT."""
        start_time = time.time()
        
        if not self._is_initialized:
            # Fallback response
            return AIModelResponse(
                text="I'm not connected to an AI model right now. Please check your configuration.",
                confidence=0.5,
                model_used="fallback",
                tokens_used=0,
                processing_time=time.time() - start_time,
                metadata={'error': 'Model not initialized'}
            )

        if not OPENAI_AVAILABLE:
            # Simulation mode
            return AIModelResponse(
                text=f"Simulated response to: {prompt}",
                confidence=0.7,
                model_used="simulation",
                tokens_used=len(prompt.split()),
                processing_time=time.time() - start_time,
                metadata={'mode': 'simulation'}
            )

        try:
            # Build messages for conversation
            messages = []
            
            # Add system context
            if context and 'system_prompt' in context:
                messages.append({"role": "system", "content": context['system_prompt']})
            else:
                messages.append({"role": "system", "content": "You are JARVIS, an AI assistant. Be helpful, concise, and accurate."})
            
            # Add conversation history
            if context and 'conversation_history' in context:
                for entry in context['conversation_history'][-5:]:  # Last 5 exchanges
                    messages.append({"role": entry.get('role', 'user'), "content": entry.get('content', '')})
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})

            # Generate response
            response = self._client.chat.completions.create(
                model=self._current_model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )

            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            processing_time = time.time() - start_time

            # Update usage stats
            self._usage_stats['total_requests'] += 1
            self._usage_stats['total_tokens'] += tokens_used
            self._usage_stats['last_request'] = datetime.now().isoformat()

            return AIModelResponse(
                text=response_text,
                confidence=0.9,
                model_used=self._current_model,
                tokens_used=tokens_used,
                processing_time=processing_time,
                metadata={'finish_reason': response.choices[0].finish_reason}
            )

        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return AIModelResponse(
                text="I encountered an error while processing your request.",
                confidence=0.0,
                model_used=self._current_model,
                tokens_used=0,
                processing_time=time.time() - start_time,
                metadata={'error': str(e)}
            )

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the given text."""
        if not self._is_initialized or not OPENAI_AVAILABLE:
            return {'sentiment': 'neutral', 'confidence': 0.5, 'score': 0.0}

        try:
            prompt = f"""Analyze the sentiment of this text and return a JSON response with:
            - sentiment: positive, negative, or neutral
            - confidence: 0.0 to 1.0
            - score: -1.0 to 1.0 (negative to positive)
            
            Text: {text}"""

            response = self.generate_response(prompt)
            
            # Try to parse JSON from response
            try:
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return result
                else:
                    # Fallback analysis
                    return self._fallback_sentiment_analysis(text)
            except json.JSONDecodeError:
                return self._fallback_sentiment_analysis(text)

        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return self._fallback_sentiment_analysis(text)

    def _fallback_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """Simple fallback sentiment analysis."""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            score = min(0.8, positive_count * 0.2)
        elif negative_count > positive_count:
            sentiment = 'negative'
            score = max(-0.8, -negative_count * 0.2)
        else:
            sentiment = 'neutral'
            score = 0.0
        
        return {
            'sentiment': sentiment,
            'confidence': 0.6,
            'score': score
        }

    def extract_intent(self, text: str) -> Dict[str, Any]:
        """Extract user intent from text."""
        if not self._is_initialized or not OPENAI_AVAILABLE:
            return {'intent': 'unknown', 'confidence': 0.5, 'entities': []}

        try:
            prompt = f"""Extract the user's intent from this text and return a JSON response with:
            - intent: the main intent (search, question, command, chat, etc.)
            - confidence: 0.0 to 1.0
            - entities: list of important entities mentioned
            
            Text: {text}"""

            response = self.generate_response(prompt)
            
            try:
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return result
                else:
                    return self._fallback_intent_extraction(text)
            except json.JSONDecodeError:
                return self._fallback_intent_extraction(text)

        except Exception as e:
            print(f"Error in intent extraction: {e}")
            return self._fallback_intent_extraction(text)

    def _fallback_intent_extraction(self, text: str) -> Dict[str, Any]:
        """Simple fallback intent extraction."""
        text_lower = text.lower()
        
        intents = {
            'search': ['search', 'find', 'look up', 'what is', 'who is'],
            'question': ['how', 'why', 'when', 'where', 'what', '?'],
            'command': ['turn on', 'turn off', 'play', 'stop', 'open', 'close'],
            'chat': ['hello', 'hi', 'how are you', 'good morning', 'good night']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in text_lower for keyword in keywords):
                return {
                    'intent': intent,
                    'confidence': 0.7,
                    'entities': []
                }
        
        return {'intent': 'unknown', 'confidence': 0.5, 'entities': []}

    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """Summarize the given text."""
        if not self._is_initialized or not OPENAI_AVAILABLE:
            # Simple fallback summarization
            words = text.split()
            if len(words) <= max_length // 5:  # Rough estimate
                return text
            return ' '.join(words[:max_length // 5]) + '...'

        try:
            prompt = f"""Summarize this text in {max_length} characters or less:
            
            {text}"""

            response = self.generate_response(prompt)
            return response.text[:max_length]

        except Exception as e:
            print(f"Error in text summarization: {e}")
            return text[:max_length] + '...' if len(text) > max_length else text

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            'name': self._current_model,
            'provider': 'OpenAI',
            'available': self._is_initialized and OPENAI_AVAILABLE,
            'max_tokens': next((m['max_tokens'] for m in self._available_models if m['name'] == self._current_model), 4096),
            'cost_per_1k': next((m['cost_per_1k'] for m in self._available_models if m['name'] == self._current_model), 0.002)
        }

    def is_available(self) -> bool:
        """Check if the AI model is available."""
        return self._is_initialized and OPENAI_AVAILABLE

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for the model."""
        return self._usage_stats.copy()

    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model."""
        available_names = [m['name'] for m in self._available_models]
        if model_name in available_names:
            self._current_model = model_name
            return True
        return False

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models."""
        return self._available_models.copy()

    def fine_tune_context(self, user_id: str, conversation_history: List[Dict[str, Any]]) -> bool:
        """Fine-tune the model context for a specific user."""
        # This would typically involve updating user-specific prompts
        # For now, we'll just store the history for future use
        return True

    def validate_response(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the generated response against context."""
        validation_result = {
            'is_valid': True,
            'confidence': 0.8,
            'issues': []
        }
        
        # Basic validation checks
        if len(response) < 10:
            validation_result['issues'].append('Response too short')
            validation_result['confidence'] -= 0.2
        
        if 'error' in response.lower() or 'sorry' in response.lower():
            validation_result['issues'].append('Response contains error indicators')
            validation_result['confidence'] -= 0.1
        
        if validation_result['confidence'] < 0.5:
            validation_result['is_valid'] = False
        
        return validation_result