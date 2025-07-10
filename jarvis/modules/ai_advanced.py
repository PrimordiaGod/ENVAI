from jarvis.interfaces.ai_model import AIModelInterface, LanguageModelInterface, PersonalizationInterface
from typing import Dict, List, Optional, Any, Union
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import time

class AdvancedAIModel(AIModelInterface, LanguageModelInterface, PersonalizationInterface):
    def __init__(self):
        self._is_initialized = False
        self._model_config = {}
        self._user_profiles = {}
        self._conversation_history = {}
        self._vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self._fitted_vectorizer = None

    def initialize(self, config: dict) -> bool:
        """Initialize the AI model with configuration."""
        try:
            self._model_config = config
            self._is_initialized = True
            return True
        except Exception as e:
            print(f"AI model initialization failed: {e}")
            return False

    def generate_response(self, prompt: str, context: dict = None) -> str:
        """Generate a response using the AI model."""
        if not self._is_initialized:
            return "I'm not ready to respond yet."
        
        # Enhanced response generation with context awareness
        if context and context.get('user_id'):
            user_id = context['user_id']
            user_profile = self.get_user_profile(user_id)
            
            # Adapt response based on user preferences
            base_response = self._generate_base_response(prompt)
            adapted_response = self.adapt_response_style(user_id, base_response)
            return adapted_response
        
        return self._generate_base_response(prompt)

    def analyze_sentiment(self, text: str) -> dict:
        """Analyze the sentiment of given text."""
        if not self._is_initialized:
            return {'sentiment': 'neutral', 'confidence': 0.0}
        
        # Simple sentiment analysis using keyword matching
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(positive_count / len(text.split()), 1.0)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(negative_count / len(text.split()), 1.0)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'positive_score': positive_count,
            'negative_score': negative_count
        }

    def extract_intent(self, text: str) -> dict:
        """Extract user intent from text."""
        if not self._is_initialized:
            return {'intent': 'unknown', 'confidence': 0.0}
        
        # Intent classification using keyword patterns
        intents = {
            'research': ['research', 'search', 'find', 'what is', 'tell me about'],
            'weather': ['weather', 'temperature', 'forecast', 'climate'],
            'schedule': ['schedule', 'calendar', 'appointment', 'meeting', 'reminder'],
            'music': ['music', 'play', 'song', 'artist', 'album'],
            'news': ['news', 'latest', 'current events', 'headlines'],
            'joke': ['joke', 'funny', 'humor', 'laugh'],
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good evening'],
            'farewell': ['goodbye', 'bye', 'see you', 'farewell']
        }
        
        text_lower = text.lower()
        best_intent = 'unknown'
        best_confidence = 0.0
        
        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            confidence = matches / len(keywords) if keywords else 0.0
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = intent
        
        return {
            'intent': best_intent,
            'confidence': best_confidence,
            'text': text
        }

    def summarize_text(self, text: str, max_length: int = 150) -> str:
        """Summarize text using AI."""
        if not self._is_initialized:
            return text[:max_length] + "..." if len(text) > max_length else text
        
        # Simple extractive summarization
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= 2:
            return text
        
        # Score sentences by word frequency
        word_freq = {}
        for sentence in sentences:
            words = sentence.lower().split()
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sentence_scores = {}
        for sentence in sentences:
            words = sentence.lower().split()
            score = sum(word_freq.get(word, 0) for word in words)
            sentence_scores[sentence] = score
        
        # Select top sentences
        sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary_sentences = []
        current_length = 0
        
        for sentence, score in sorted_sentences:
            if current_length + len(sentence) <= max_length:
                summary_sentences.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        return '. '.join(summary_sentences) + '.'

    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language."""
        # Placeholder for translation (in real implementation, would use translation API)
        return f"[Translated to {target_language}: {text}]"

    def classify_text(self, text: str, categories: List[str]) -> dict:
        """Classify text into predefined categories."""
        if not self._is_initialized:
            return {'category': 'unknown', 'confidence': 0.0}
        
        # Simple classification using keyword matching
        text_lower = text.lower()
        category_scores = {}
        
        for category in categories:
            # Define keywords for each category
            category_keywords = {
                'technology': ['computer', 'software', 'hardware', 'programming', 'ai', 'machine learning'],
                'science': ['research', 'experiment', 'discovery', 'scientific', 'study'],
                'business': ['company', 'profit', 'market', 'investment', 'strategy'],
                'entertainment': ['movie', 'music', 'game', 'fun', 'entertainment'],
                'sports': ['game', 'team', 'player', 'score', 'championship']
            }
            
            keywords = category_keywords.get(category, [])
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            score = matches / len(keywords) if keywords else 0.0
            category_scores[category] = score
        
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            confidence = category_scores[best_category]
        else:
            best_category = 'unknown'
            confidence = 0.0
        
        return {
            'category': best_category,
            'confidence': confidence,
            'scores': category_scores
        }

    def get_model_info(self) -> dict:
        """Get information about the AI model."""
        return {
            'name': 'Advanced AI Model',
            'version': '1.0',
            'capabilities': ['sentiment_analysis', 'intent_extraction', 'text_summarization', 'personalization'],
            'initialized': self._is_initialized
        }

    # Language Model Interface Methods
    def load_model(self, model_name: str) -> bool:
        """Load a specific language model."""
        # Placeholder for model loading
        print(f"Loading model: {model_name}")
        return True

    def generate_completion(self, prompt: str, max_tokens: int = 100) -> str:
        """Generate text completion."""
        # Simple completion using pattern matching
        completions = {
            'hello': 'Hello! How can I help you today?',
            'weather': 'The weather is currently sunny with a temperature of 72°F.',
            'time': f'The current time is {time.strftime("%H:%M")}.',
            'help': 'I can help you with research, weather, scheduling, and more!'
        }
        
        prompt_lower = prompt.lower()
        for key, completion in completions.items():
            if key in prompt_lower:
                return completion
        
        return "I understand you said: " + prompt

    def generate_embedding(self, text: str) -> List[float]:
        """Generate text embeddings."""
        # Simple TF-IDF based embedding
        if not self._fitted_vectorizer:
            # Fit vectorizer with sample texts
            sample_texts = [text] + ["sample text for fitting"]
            self._fitted_vectorizer = self._vectorizer.fit(sample_texts)
        
        embedding = self._fitted_vectorizer.transform([text]).toarray()[0]
        return embedding.tolist()

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        embedding1 = self.generate_embedding(text1)
        embedding2 = self.generate_embedding(text2)
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        return float(similarity)

    # Personalization Interface Methods
    def learn_user_patterns(self, user_id: str, data: dict) -> bool:
        """Learn patterns from user data."""
        if user_id not in self._user_profiles:
            self._user_profiles[user_id] = {
                'preferences': {},
                'conversation_style': {},
                'interests': set(),
                'interaction_count': 0
            }
        
        profile = self._user_profiles[user_id]
        profile['interaction_count'] += 1
        
        # Learn from conversation data
        if 'text' in data:
            sentiment = self.analyze_sentiment(data['text'])
            intent = self.extract_intent(data['text'])
            
            # Update preferences based on sentiment and intent
            if sentiment['sentiment'] == 'positive':
                profile['preferences']['positive_interactions'] = profile['preferences'].get('positive_interactions', 0) + 1
            
            if intent['intent'] != 'unknown':
                profile['preferences']['favorite_intents'] = profile['preferences'].get('favorite_intents', {})
                profile['preferences']['favorite_intents'][intent['intent']] = profile['preferences']['favorite_intents'].get(intent['intent'], 0) + 1
        
        return True

    def predict_user_preferences(self, user_id: str, context: dict) -> dict:
        """Predict user preferences based on learned patterns."""
        if user_id not in self._user_profiles:
            return {}
        
        profile = self._user_profiles[user_id]
        predictions = {
            'preferred_response_style': 'formal' if profile['interaction_count'] < 5 else 'casual',
            'likely_intents': [],
            'sentiment_preference': 'neutral'
        }
        
        # Predict based on learned patterns
        if 'favorite_intents' in profile['preferences']:
            sorted_intents = sorted(profile['preferences']['favorite_intents'].items(), 
                                  key=lambda x: x[1], reverse=True)
            predictions['likely_intents'] = [intent for intent, count in sorted_intents[:3]]
        
        if profile['preferences'].get('positive_interactions', 0) > 5:
            predictions['sentiment_preference'] = 'positive'
        
        return predictions

    def adapt_response_style(self, user_id: str, base_response: str) -> str:
        """Adapt response style to user preferences."""
        preferences = self.predict_user_preferences(user_id, {})
        
        if preferences.get('preferred_response_style') == 'casual':
            # Make response more casual
            base_response = base_response.replace("I can", "I can totally")
            base_response = base_response.replace("Hello", "Hey there")
        
        if preferences.get('sentiment_preference') == 'positive':
            # Add positive elements
            if not any(word in base_response.lower() for word in ['great', 'awesome', 'excellent']):
                base_response += " That's great!"
        
        return base_response

    def get_user_profile(self, user_id: str) -> dict:
        """Get user's learned profile."""
        if user_id not in self._user_profiles:
            return {}
        
        profile = self._user_profiles[user_id].copy()
        # Convert set to list for JSON serialization
        if 'interests' in profile:
            profile['interests'] = list(profile['interests'])
        
        return profile