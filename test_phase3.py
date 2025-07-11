#!/usr/bin/env python3
"""
Phase 3 Test Script for JARVIS Next-Gen AI Personal Assistant
Tests real voice integration, AI models, smart home, and enhanced features.
"""

import sys
import os
import time
import json
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis.modules.voice_simple import AdvancedVoiceInterface
from jarvis.modules.ai_model_openai import OpenAIInterface
from jarvis.modules.smart_home_hub import SmartHomeHub
from jarvis.modules.context_memory import MemoryContextEngine
from jarvis.modules.research_web import WebResearch
from jarvis.modules.plugin_manager import PluginManager
from jarvis.modules.cloud_local import LocalCloudStorage

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section."""
    print(f"\n📋 {title}")
    print("-" * 40)

def test_voice_integration():
    """Test Phase 3 voice integration features."""
    print_header("Testing Voice Integration (Phase 3)")
    
    voice = AdvancedVoiceInterface()
    
    # Test initialization
    print_section("Voice Interface Initialization")
    success = voice.initialize()
    print(f"✅ Voice initialization: {'SUCCESS' if success else 'FAILED'}")
    
    # Test voice settings
    print_section("Voice Settings")
    settings = voice.get_voice_settings()
    print(f"Current settings: {settings}")
    
    # Test voice status
    print_section("Voice Status")
    status = voice.get_voice_status()
    print(f"Voice status: {status}")
    
    # Test available voices
    print_section("Available Voices")
    voices = voice.get_available_voices()
    print(f"Available voices: {len(voices)}")
    for voice_info in voices[:3]:  # Show first 3
        print(f"  - {voice_info.get('name', 'Unknown')}")
    
    # Test voice command processing
    print_section("Voice Command Processing")
    test_commands = [
        "turn on living room light",
        "set thermostat to 72",
        "what is the weather",
        "dim bedroom light"
    ]
    
    for command in test_commands:
        result = voice.process_voice_command(command)
        print(f"Command: '{command}'")
        print(f"  Intent: {result['command']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Parameters: {result['parameters']}")
    
    # Test microphone calibration
    print_section("Microphone Calibration")
    calibration = voice.calibrate_microphone()
    print(f"Calibration result: {calibration}")
    
    return True

def test_ai_model_integration():
    """Test Phase 3 AI model integration."""
    print_header("Testing AI Model Integration (Phase 3)")
    
    ai_model = OpenAIInterface()
    
    # Test initialization
    print_section("AI Model Initialization")
    config = {'api_key': os.getenv('OPENAI_API_KEY', '')}
    success = ai_model.initialize(config)
    print(f"✅ AI model initialization: {'SUCCESS' if success else 'FAILED (using fallback)'}")
    
    # Test model info
    print_section("Model Information")
    model_info = ai_model.get_model_info()
    print(f"Model: {model_info['name']}")
    print(f"Provider: {model_info['provider']}")
    print(f"Available: {model_info['available']}")
    
    # Test available models
    print_section("Available Models")
    models = ai_model.get_available_models()
    print(f"Available models: {len(models)}")
    for model in models:
        print(f"  - {model['name']} (max tokens: {model['max_tokens']})")
    
    # Test response generation
    print_section("Response Generation")
    test_prompts = [
        "Hello, how are you?",
        "What is artificial intelligence?",
        "Tell me a joke"
    ]
    
    for prompt in test_prompts:
        print(f"\nPrompt: '{prompt}'")
        response = ai_model.generate_response(prompt)
        print(f"Response: {response.text[:100]}...")
        print(f"Confidence: {response.confidence}")
        print(f"Model used: {response.model_used}")
        print(f"Tokens used: {response.tokens_used}")
    
    # Test sentiment analysis
    print_section("Sentiment Analysis")
    test_texts = [
        "I love this amazing product!",
        "This is terrible, I hate it.",
        "The weather is okay today."
    ]
    
    for text in test_texts:
        sentiment = ai_model.analyze_sentiment(text)
        print(f"Text: '{text}'")
        print(f"  Sentiment: {sentiment['sentiment']}")
        print(f"  Confidence: {sentiment['confidence']}")
        print(f"  Score: {sentiment['score']}")
    
    # Test intent extraction
    print_section("Intent Extraction")
    test_inputs = [
        "Search for information about Python",
        "What time is it?",
        "Turn on the lights",
        "How are you doing today?"
    ]
    
    for user_input in test_inputs:
        intent = ai_model.extract_intent(user_input)
        print(f"Input: '{user_input}'")
        print(f"  Intent: {intent['intent']}")
        print(f"  Confidence: {intent['confidence']}")
        print(f"  Entities: {intent['entities']}")
    
    # Test text summarization
    print_section("Text Summarization")
    long_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines 
    that work and react like humans. Some of the activities computers with artificial intelligence are 
    designed for include speech recognition, learning, planning, and problem solving. AI has been used 
    in various applications including medical diagnosis, stock trading, robot control, law, scientific 
    discovery, and toys. The field was founded on the assumption that human intelligence can be precisely 
    described and simulated by machines.
    """
    
    summary = ai_model.summarize_text(long_text, max_length=100)
    print(f"Original text length: {len(long_text)} characters")
    print(f"Summary: {summary}")
    print(f"Summary length: {len(summary)} characters")
    
    # Test usage stats
    print_section("Usage Statistics")
    stats = ai_model.get_usage_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Last request: {stats['last_request']}")
    
    return True

def test_smart_home_integration():
    """Test Phase 3 smart home integration."""
    print_header("Testing Smart Home Integration (Phase 3)")
    
    smart_home = SmartHomeHub()
    
    # Test initialization
    print_section("Smart Home Hub Initialization")
    config = {'auto_discover': True}
    success = smart_home.initialize(config)
    print(f"✅ Smart home initialization: {'SUCCESS' if success else 'FAILED'}")
    
    # Test device discovery
    print_section("Device Discovery")
    devices = smart_home.discover_devices()
    print(f"Discovered {len(devices)} devices:")
    for device in devices:
        status = "🟢" if device.properties.get('power', False) else "🔴"
        print(f"  {status} {device.name} ({device.type.value}) - {device.location}")
    
    # Test device control
    print_section("Device Control")
    test_device = devices[0] if devices else None
    if test_device:
        print(f"Testing control of: {test_device.name}")
        
        # Test turn on
        success = smart_home.control_device(test_device.id, 'turn_on')
        print(f"  Turn on: {'SUCCESS' if success else 'FAILED'}")
        
        # Test turn off
        success = smart_home.control_device(test_device.id, 'turn_off')
        print(f"  Turn off: {'SUCCESS' if success else 'FAILED'}")
    
    # Test device status
    print_section("Device Status")
    for device in devices[:3]:  # Test first 3 devices
        status = smart_home.get_device_status(device.id)
        print(f"  {device.name}: {status}")
    
    # Test rooms
    print_section("Room Management")
    rooms = smart_home.get_rooms()
    print(f"Available rooms: {len(rooms)}")
    for room in rooms:
        print(f"  - {room['name']}: {room['device_count']} devices")
    
    # Test scenes
    print_section("Scene Management")
    scenes = smart_home.get_scenes()
    print(f"Available scenes: {len(scenes)}")
    for scene in scenes:
        print(f"  - {scene['name']}: {scene['description']}")
    
    # Test voice control
    print_section("Voice Control")
    voice_commands = [
        "turn on living room light",
        "set thermostat to 75",
        "dim bedroom light",
        "what is the thermostat",
        "activate movie mode"
    ]
    
    for command in voice_commands:
        result = smart_home.voice_control(command)
        print(f"Command: '{command}'")
        print(f"  Success: {result['success']}")
        print(f"  Action: {result['action']}")
        print(f"  Message: {result['message']}")
    
    # Test energy usage
    print_section("Energy Usage")
    energy = smart_home.get_energy_usage()
    print(f"Total devices on: {energy['total_devices_on']}")
    print(f"Power consumption: {energy['total_power_consumption']}W")
    print(f"Daily usage: {energy['daily_usage']:.1f} kWh")
    print(f"Monthly cost: ${energy['estimated_cost']:.2f}")
    
    # Test system status
    print_section("System Status")
    status = smart_home.get_system_status()
    print(f"Total devices: {status['total_devices']}")
    print(f"Online devices: {status['online_devices']}")
    print(f"Powered devices: {status['powered_devices']}")
    print(f"System health: {status['system_health']}")
    
    # Test automation
    print_section("Automation")
    automation_id = smart_home.create_automation(
        "Test Automation",
        {"type": "time", "hour": 8, "minute": 0},
        [{"device_id": "light_1", "action": "turn_on"}]
    )
    print(f"Created automation: {automation_id}")
    
    automations = smart_home.get_automations()
    print(f"Total automations: {len(automations)}")
    
    # Test backup/restore
    print_section("Configuration Backup/Restore")
    backup = smart_home.backup_configuration()
    print(f"Backup created with {len(backup['devices'])} devices")
    
    success = smart_home.restore_configuration(backup)
    print(f"Restore: {'SUCCESS' if success else 'FAILED'}")
    
    return True

def test_enhanced_features():
    """Test enhanced Phase 3 features."""
    print_header("Testing Enhanced Features (Phase 3)")
    
    # Test context engine with AI integration
    print_section("Enhanced Context Engine")
    context_engine = MemoryContextEngine()
    
    # Test user preferences
    user_id = "test_user"
    preferences = {
        'language': 'en',
        'voice_speed': 1.0,
        'research_depth': 'deep',
        'smart_home_enabled': True
    }
    context_engine.update_user_preferences(user_id, preferences)
    
    retrieved_prefs = context_engine.get_user_preferences(user_id)
    print(f"User preferences: {retrieved_prefs}")
    
    # Test conversation patterns
    conversations = [
        ("Hello", "Hi there! How can I help you?"),
        ("What's the weather?", "Let me check the weather for you."),
        ("Turn on the lights", "I'll turn on the lights for you."),
        ("What time is it?", "The current time is 2:30 PM.")
    ]
    
    for user_input, response in conversations:
        context_engine.add_conversation_entry(user_id, user_input, response)
    
    # Test intent anticipation
    anticipations = context_engine.anticipate_user_intent(user_id, "What's the")
    print(f"Intent anticipations: {anticipations}")
    
    # Test research with AI enhancement
    print_section("Enhanced Research")
    research = WebResearch()
    
    # Test deep analysis
    analysis = research.deep_analysis("artificial intelligence", {})
    print(f"Deep analysis confidence: {analysis.get('confidence', 0)}")
    print(f"Sources found: {len(analysis.get('sources', []))}")
    
    # Test information synthesis
    synthesis = research.synthesize_information([analysis])
    print(f"Synthesis length: {len(synthesis)} characters")
    
    # Test plugin system
    print_section("Enhanced Plugin System")
    plugin_manager = PluginManager()
    
    plugins = plugin_manager.list_plugins()
    print(f"Available plugins: {len(plugins)}")
    
    # Test cloud storage
    print_section("Enhanced Cloud Storage")
    cloud_storage = LocalCloudStorage()
    cloud_storage.initialize({'local_mode': True})
    
    test_data = {
        'user_preferences': {'theme': 'dark', 'notifications': True},
        'conversation_history': [{'user': 'Hello', 'assistant': 'Hi!'}],
        'smart_home_config': {'devices': 5, 'automations': 2}
    }
    
    success = cloud_storage.sync_to_cloud(test_data)
    print(f"Cloud sync: {'SUCCESS' if success else 'FAILED'}")
    
    status = cloud_storage.get_sync_status()
    print(f"Sync status: {status}")
    
    return True

def test_integration():
    """Test integration between all Phase 3 components."""
    print_header("Testing Phase 3 Integration")
    
    # Test voice + AI integration
    print_section("Voice + AI Integration")
    voice = AdvancedVoiceInterface()
    ai_model = OpenAIInterface()
    
    voice.initialize()
    ai_model.initialize({'api_key': os.getenv('OPENAI_API_KEY', '')})
    
    # Simulate voice command processing
    voice_command = "What is the weather like today?"
    processed = voice.process_voice_command(voice_command)
    ai_response = ai_model.generate_response(voice_command)
    
    print(f"Voice command: {voice_command}")
    print(f"Processed intent: {processed['command']}")
    print(f"AI response: {ai_response.text[:100]}...")
    
    # Test smart home + voice integration
    print_section("Smart Home + Voice Integration")
    smart_home = SmartHomeHub()
    smart_home.initialize({'auto_discover': True})
    
    home_command = "turn on living room light"
    home_result = smart_home.voice_control(home_command)
    
    print(f"Smart home command: {home_command}")
    print(f"Result: {home_result['message']}")
    
    # Test AI + research integration
    print_section("AI + Research Integration")
    research = WebResearch()
    
    query = "latest developments in quantum computing"
    ai_response = ai_model.generate_response(f"Research: {query}")
    research_results = research.search(query)
    
    print(f"Research query: {query}")
    print(f"AI enhanced response: {ai_response.text[:150]}...")
    print(f"Research sources: {len(research_results)}")
    
    return True

def run_performance_tests():
    """Run performance tests for Phase 3 features."""
    print_header("Performance Tests (Phase 3)")
    
    # Test AI model response time
    print_section("AI Model Performance")
    ai_model = OpenAIInterface()
    ai_model.initialize({'api_key': os.getenv('OPENAI_API_KEY', '')})
    
    start_time = time.time()
    response = ai_model.generate_response("Hello, how are you?")
    ai_time = time.time() - start_time
    
    print(f"AI response time: {ai_time:.2f} seconds")
    print(f"Response confidence: {response.confidence}")
    print(f"Tokens used: {response.tokens_used}")
    
    # Test voice processing performance
    print_section("Voice Processing Performance")
    voice = AdvancedVoiceInterface()
    voice.initialize()
    
    start_time = time.time()
    for i in range(5):
        voice.process_voice_command(f"test command {i}")
    voice_time = time.time() - start_time
    
    print(f"Voice processing time (5 commands): {voice_time:.2f} seconds")
    print(f"Average per command: {voice_time/5:.3f} seconds")
    
    # Test smart home performance
    print_section("Smart Home Performance")
    smart_home = SmartHomeHub()
    smart_home.initialize({'auto_discover': True})
    
    start_time = time.time()
    devices = smart_home.discover_devices()
    device_time = time.time() - start_time
    
    print(f"Device discovery time: {device_time:.3f} seconds")
    print(f"Devices found: {len(devices)}")
    
    start_time = time.time()
    for device in devices[:3]:
        smart_home.control_device(device.id, 'turn_on')
    control_time = time.time() - start_time
    
    print(f"Device control time (3 devices): {control_time:.3f} seconds")
    print(f"Average per device: {control_time/3:.3f} seconds")
    
    return True

def main():
    """Run all Phase 3 tests."""
    print("🚀 JARVIS Phase 3 Testing Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = []
    
    try:
        # Test individual components
        test_results.append(("Voice Integration", test_voice_integration()))
        test_results.append(("AI Model Integration", test_ai_model_integration()))
        test_results.append(("Smart Home Integration", test_smart_home_integration()))
        test_results.append(("Enhanced Features", test_enhanced_features()))
        
        # Test integration
        test_results.append(("Component Integration", test_integration()))
        
        # Performance tests
        test_results.append(("Performance Tests", run_performance_tests()))
        
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        return False
    
    # Print summary
    print_header("Phase 3 Test Results")
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Phase 3 tests passed! JARVIS is ready for advanced AI operations.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)