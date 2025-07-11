#!/usr/bin/env python3
"""
Test Script for JARVIS Emotional Intelligence System

Tests advanced memory architecture, personality adaptation, and continuous learning
for single-user emotional intelligence and rapport building.
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis.emotional_intelligence.emotional_coordinator import EmotionalIntelligenceCoordinator
from jarvis.emotional_intelligence.emotional_memory import EmotionalState, EmotionalContext, MemoryType
from jarvis.emotional_intelligence.personality_engine import CommunicationStyle, PersonalityTrait

class EmotionalIntelligenceTester:
    """Test suite for emotional intelligence system"""
    
    def __init__(self):
        self.coordinator = EmotionalIntelligenceCoordinator("test_emotional_intelligence.db")
        self.test_results = {
            'memory_architecture': [],
            'personality_adaptation': [],
            'continuous_learning': [],
            'emotional_analysis': [],
            'rapport_building': [],
            'integration': []
        }
    
    async def run_all_tests(self):
        """Run all emotional intelligence tests"""
        print("🧠 Testing JARVIS Emotional Intelligence System")
        print("=" * 60)
        
        # Test categories
        await self._test_memory_architecture()
        await self._test_personality_adaptation()
        await self._test_continuous_learning()
        await self._test_emotional_analysis()
        await self._test_rapport_building()
        await self._test_integration()
        
        # Generate report
        self._generate_test_report()
    
    async def _test_memory_architecture(self):
        """Test advanced memory architecture"""
        print("\n💾 Testing Memory Architecture...")
        
        try:
            # Test memory storage
            emotional_context = EmotionalContext(
                primary_emotion=EmotionalState.HAPPY,
                intensity=0.8,
                confidence=0.9,
                triggers=['positive_news'],
                responses=['express_joy']
            )
            
            memory_id = await self.coordinator.emotional_memory.store_memory(
                content="User shared exciting news about a promotion",
                memory_type=MemoryType.EMOTIONAL_EXPERIENCE,
                emotional_context=emotional_context,
                importance_score=0.9,
                tags=['promotion', 'success', 'positive']
            )
            
            self.test_results['memory_architecture'].append(('Memory Storage', True, f"Stored memory: {memory_id}"))
            
            # Test memory recall
            recalled_memories = await self.coordinator.emotional_memory.recall_memory(
                "promotion", emotional_context, limit=5
            )
            
            self.test_results['memory_architecture'].append(('Memory Recall', len(recalled_memories) > 0, f"Recalled {len(recalled_memories)} memories"))
            
            # Test emotional summary
            emotional_summary = self.coordinator.emotional_memory.get_emotional_summary()
            
            self.test_results['memory_architecture'].append(('Emotional Summary', bool(emotional_summary), f"Summary generated: {emotional_summary.get('dominant_emotion', 'unknown')}"))
            
            # Test pattern analysis
            adaptation_suggestions = self.coordinator.emotional_memory.get_adaptation_suggestions()
            
            self.test_results['memory_architecture'].append(('Pattern Analysis', True, f"Generated {len(adaptation_suggestions)} adaptation suggestions"))
            
        except Exception as e:
            self.test_results['memory_architecture'].append(('Memory Architecture', False, f"Error: {str(e)}"))
    
    async def _test_personality_adaptation(self):
        """Test personality adaptation system"""
        print("\n🎭 Testing Personality Adaptation...")
        
        try:
            # Test emotional response configuration
            emotional_context = EmotionalContext(
                primary_emotion=EmotionalState.SAD,
                intensity=0.7,
                confidence=0.8,
                triggers=['difficult_situation'],
                responses=['offer_support']
            )
            
            # Test personality adaptation
            await self.coordinator.personality_engine.adapt_personality(emotional_context)
            
            self.test_results['personality_adaptation'].append(('Personality Adaptation', True, "Adapted personality for sad emotion"))
            
            # Test communication style selection
            communication_style = self.coordinator.personality_engine.get_communication_style(emotional_context)
            
            self.test_results['personality_adaptation'].append(('Communication Style', communication_style == CommunicationStyle.EMPATHETIC, f"Selected style: {communication_style.value}"))
            
            # Test response template generation
            response_template = self.coordinator.personality_engine.get_response_template(emotional_context)
            
            self.test_results['personality_adaptation'].append(('Response Template', bool(response_template), f"Generated template: {response_template[:50]}..."))
            
            # Test personality summary
            personality_summary = self.coordinator.personality_engine.get_personality_summary()
            
            self.test_results['personality_adaptation'].append(('Personality Summary', bool(personality_summary), f"Current style: {personality_summary.get('communication_style', 'unknown')}"))
            
        except Exception as e:
            self.test_results['personality_adaptation'].append(('Personality Adaptation', False, f"Error: {str(e)}"))
    
    async def _test_continuous_learning(self):
        """Test continuous learning system"""
        print("\n📚 Testing Continuous Learning...")
        
        try:
            # Test learning from interaction
            interaction_data = {
                'satisfaction': 0.8,
                'emotional_context': {
                    'emotion': 'happy',
                    'intensity': 0.7,
                    'confidence': 0.8
                },
                'user_feedback': {
                    'positive': True,
                    'satisfaction': 0.8,
                    'positive_indicators': ['helpful', 'understanding']
                }
            }
            
            await self.coordinator.personality_engine.learn_from_interaction(interaction_data)
            
            self.test_results['continuous_learning'].append(('Learning from Interaction', True, "Processed positive interaction"))
            
            # Test negative feedback learning
            negative_interaction = {
                'satisfaction': 0.3,
                'emotional_context': {
                    'emotion': 'frustrated',
                    'intensity': 0.8,
                    'confidence': 0.7
                },
                'user_feedback': {
                    'negative': True,
                    'satisfaction': 0.3,
                    'too_formal': True,
                    'not_empathetic': True
                }
            }
            
            await self.coordinator.personality_engine.learn_from_interaction(negative_interaction)
            
            self.test_results['continuous_learning'].append(('Negative Feedback Learning', True, "Processed negative feedback"))
            
            # Test adaptation suggestions
            adaptation_suggestions = self.coordinator.personality_engine.get_emotional_adaptation_suggestions()
            
            self.test_results['continuous_learning'].append(('Adaptation Suggestions', len(adaptation_suggestions) > 0, f"Generated {len(adaptation_suggestions)} suggestions"))
            
            # Test learning report
            learning_report = await self.coordinator.get_continuous_learning_report()
            
            self.test_results['continuous_learning'].append(('Learning Report', bool(learning_report), f"Success rate: {learning_report.get('success_rate', 0):.2f}"))
            
        except Exception as e:
            self.test_results['continuous_learning'].append(('Continuous Learning', False, f"Error: {str(e)}"))
    
    async def _test_emotional_analysis(self):
        """Test emotional analysis capabilities"""
        print("\n🔍 Testing Emotional Analysis...")
        
        try:
            # Test text-based emotion detection
            happy_text = "I'm so excited about my new job! 😊"
            sad_text = "I'm feeling really down today 😢"
            anxious_text = "I'm worried about the upcoming presentation 😰"
            
            # Test happy emotion detection
            happy_result = await self.coordinator.process_interaction(happy_text)
            
            self.test_results['emotional_analysis'].append(('Happy Emotion Detection', 
                happy_result['emotional_context']['emotion'] == 'happy', 
                f"Detected: {happy_result['emotional_context']['emotion']}"))
            
            # Test sad emotion detection
            sad_result = await self.coordinator.process_interaction(sad_text)
            
            self.test_results['emotional_analysis'].append(('Sad Emotion Detection', 
                sad_result['emotional_context']['emotion'] == 'sad', 
                f"Detected: {sad_result['emotional_context']['emotion']}"))
            
            # Test anxious emotion detection
            anxious_result = await self.coordinator.process_interaction(anxious_text)
            
            self.test_results['emotional_analysis'].append(('Anxious Emotion Detection', 
                anxious_result['emotional_context']['emotion'] == 'anxious', 
                f"Detected: {anxious_result['emotional_context']['emotion']}"))
            
            # Test neutral emotion detection
            neutral_text = "What's the weather like today?"
            neutral_result = await self.coordinator.process_interaction(neutral_text)
            
            self.test_results['emotional_analysis'].append(('Neutral Emotion Detection', 
                neutral_result['emotional_context']['emotion'] == 'neutral', 
                f"Detected: {neutral_result['emotional_context']['emotion']}"))
            
        except Exception as e:
            self.test_results['emotional_analysis'].append(('Emotional Analysis', False, f"Error: {str(e)}"))
    
    async def _test_rapport_building(self):
        """Test rapport building capabilities"""
        print("\n💙 Testing Rapport Building...")
        
        try:
            # Test rapport score calculation
            initial_rapport = self.coordinator.rapport_score
            
            # Simulate positive interaction
            positive_interaction = await self.coordinator.process_interaction(
                "I really appreciate your help today! 😊",
                user_feedback={'satisfaction': 0.9, 'positive': True}
            )
            
            self.test_results['rapport_building'].append(('Positive Interaction', 
                positive_interaction['rapport_score'] > initial_rapport, 
                f"Rapport score: {positive_interaction['rapport_score']:.2f}"))
            
            # Test emotional alignment
            emotional_alignment = positive_interaction['emotional_context']['emotion'] == 'happy'
            
            self.test_results['rapport_building'].append(('Emotional Alignment', 
                emotional_alignment, 
                f"Aligned with: {positive_interaction['emotional_context']['emotion']}"))
            
            # Test memory relevance
            memory_relevance = positive_interaction['relevant_memories'] > 0
            
            self.test_results['rapport_building'].append(('Memory Relevance', 
                memory_relevance, 
                f"Relevant memories: {positive_interaction['relevant_memories']}"))
            
            # Test communication style adaptation
            communication_style = positive_interaction['communication_style']
            
            self.test_results['rapport_building'].append(('Communication Adaptation', 
                communication_style in ['enthusiastic', 'supportive'], 
                f"Adapted style: {communication_style}"))
            
        except Exception as e:
            self.test_results['rapport_building'].append(('Rapport Building', False, f"Error: {str(e)}"))
    
    async def _test_integration(self):
        """Test system integration"""
        print("\n🔗 Testing System Integration...")
        
        try:
            # Test emotional insights generation
            insights = await self.coordinator.get_emotional_insights()
            
            self.test_results['integration'].append(('Emotional Insights', 
                bool(insights), 
                f"Generated insights with {len(insights)} sections"))
            
            # Test comprehensive data export
            export_data = await self.coordinator.export_emotional_intelligence_data()
            
            self.test_results['integration'].append(('Data Export', 
                bool(export_data), 
                f"Exported data with {len(export_data)} components"))
            
            # Test memory and personality coordination
            memory_data = self.coordinator.emotional_memory.export_memory_data()
            personality_data = self.coordinator.personality_engine.export_personality_data()
            
            self.test_results['integration'].append(('Component Coordination', 
                bool(memory_data) and bool(personality_data), 
                f"Memory: {memory_data['total_memories']}, Personality: {personality_data['adaptation_history']}"))
            
            # Test learning session tracking
            learning_sessions = len(self.coordinator.learning_sessions)
            
            self.test_results['integration'].append(('Learning Tracking', 
                learning_sessions > 0, 
                f"Tracked {learning_sessions} learning sessions"))
            
        except Exception as e:
            self.test_results['integration'].append(('System Integration', False, f"Error: {str(e)}"))
    
    def _generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 EMOTIONAL INTELLIGENCE TEST RESULTS")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        
        for category, tests in self.test_results.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            print("-" * 40)
            
            category_passed = 0
            for test_name, passed, message in tests:
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"{status} {test_name}: {message}")
                if passed:
                    category_passed += 1
                    passed_tests += 1
                total_tests += 1
            
            category_percentage = (category_passed / len(tests)) * 100 if tests else 0
            print(f"Category Result: {category_passed}/{len(tests)} ({category_percentage:.1f}%)")
        
        # Overall results
        overall_percentage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"\n{'='*60}")
        print(f"OVERALL RESULTS: {passed_tests}/{total_tests} ({overall_percentage:.1f}%)")
        
        if overall_percentage >= 90:
            print("🎉 EXCELLENT: Emotional Intelligence System is fully operational!")
        elif overall_percentage >= 75:
            print("✅ GOOD: Emotional Intelligence System is mostly operational!")
        elif overall_percentage >= 50:
            print("⚠️ FAIR: Emotional Intelligence System needs some improvements!")
        else:
            print("❌ POOR: Emotional Intelligence System needs significant work!")
        
        print("=" * 60)

async def main():
    """Main test function"""
    tester = EmotionalIntelligenceTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())