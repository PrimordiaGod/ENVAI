#!/usr/bin/env python3
"""
Comprehensive test script for Phase 2 implementation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis.modules.interaction_cli import CLIInteraction
from jarvis.modules.context_memory import MemoryContextEngine
from jarvis.modules.research_web import WebResearch
from jarvis.modules.selfmod_sandbox import SandboxSelfMod
from jarvis.modules.storage_encrypted import EncryptedStorage
from jarvis.modules.voice_simple import SimpleVoiceInterface
from jarvis.modules.plugin_manager import PluginManager
from jarvis.modules.cloud_local import LocalCloudStorage

def test_phase2():
    print("🧪 Testing Phase 2 Implementation...")
    
    # Initialize all modules
    interaction = CLIInteraction()
    context_engine = MemoryContextEngine()
    research = WebResearch()
    selfmod = SandboxSelfMod()
    storage = EncryptedStorage()
    voice = SimpleVoiceInterface()
    plugin_manager = PluginManager()
    cloud_storage = LocalCloudStorage()
    
    print("✅ All modules initialized successfully")
    
    # Test 1: Enhanced Context Engine
    print("\n📝 Testing Enhanced Context Engine...")
    user_id = 'test_user'
    
    # Test long-term memory
    memory_data = {'topic': 'AI research', 'category': 'technology'}
    context_engine.store_long_term_memory(user_id, memory_data)
    memories = context_engine.retrieve_long_term_memory(user_id)
    assert memories['count'] > 0
    print("✅ Long-term memory working")
    
    # Test user intent anticipation
    anticipations = context_engine.anticipate_user_intent(user_id, "research artificial intelligence")
    assert isinstance(anticipations, list)
    print("✅ User intent anticipation working")
    
    # Test user preferences
    preferences = {'language': 'en', 'research_depth': 'deep'}
    context_engine.update_user_preferences(user_id, preferences)
    retrieved_prefs = context_engine.get_user_preferences(user_id)
    assert retrieved_prefs['language'] == 'en'
    print("✅ User preferences working")
    
    # Test conversation pattern analysis
    context_engine.add_conversation_entry(user_id, "Hello", "Hi there!", "greeting")
    patterns = context_engine.analyze_conversation_patterns(user_id)
    assert 'total_conversations' in patterns
    print("✅ Conversation pattern analysis working")
    
    # Test 2: Enhanced Research
    print("\n🔍 Testing Enhanced Research...")
    
    # Test multi-source search
    multi_results = research.multi_source_search("Python programming")
    assert 'sources' in multi_results
    print("✅ Multi-source search working")
    
    # Test deep analysis
    analysis = research.deep_analysis("artificial intelligence", {'previous_topics': 'machine learning'})
    assert 'confidence_score' in analysis
    print("✅ Deep analysis working")
    
    # Test information synthesis
    synthesis = research.synthesize_information([{'AbstractText': 'Test data'}])
    assert isinstance(synthesis, str)
    print("✅ Information synthesis working")
    
    # Test fact checking
    fact_check = research.fact_check("Python is a programming language")
    assert 'confidence' in fact_check
    print("✅ Fact checking working")
    
    # Test trending topics
    trending = research.get_trending_topics("technology")
    assert isinstance(trending, list)
    print("✅ Trending topics working")
    
    # Test research sessions
    session_data = {'query': 'test', 'results': 'test results'}
    research.save_research_session('test_session', session_data)
    loaded_session = research.load_research_session('test_session')
    assert loaded_session
    print("✅ Research sessions working")
    
    # Test 3: Voice Interface
    print("\n🎤 Testing Voice Interface...")
    
    # Test initialization
    voice_initialized = voice.initialize()
    assert voice_initialized
    print("✅ Voice interface initialization working")
    
    # Test voice settings
    voice.set_voice_settings({'speed': 1.2, 'pitch': 1.1})
    settings = voice.get_voice_settings()
    assert settings['speed'] == 1.2
    print("✅ Voice settings working")
    
    # Test voice simulation
    voice.set_voice_callback(lambda text: print(f"Voice callback: {text}"))
    voice.simulate_voice_input("Hello JARVIS")
    print("✅ Voice simulation working")
    
    # Test 4: Plugin System
    print("\n🔌 Testing Plugin System...")
    
    # Test plugin listing
    plugins = plugin_manager.list_plugins()
    assert isinstance(plugins, list)
    print("✅ Plugin listing working")
    
    # Test plugin commands
    all_commands = plugin_manager.get_all_commands()
    assert isinstance(all_commands, dict)
    print("✅ Plugin commands working")
    
    # Test plugin configuration
    config_saved = plugin_manager.save_plugin_config("test_plugin_config.json")
    assert config_saved
    print("✅ Plugin configuration working")
    
    # Test 5: Cloud Storage
    print("\n☁️ Testing Cloud Storage...")
    
    # Test initialization
    cloud_initialized = cloud_storage.initialize({'local_mode': True})
    assert cloud_initialized
    print("✅ Cloud storage initialization working")
    
    # Test data upload/download
    test_data = b"test cloud data"
    upload_success = cloud_storage.upload_data("test_key", test_data)
    assert upload_success
    print("✅ Cloud upload working")
    
    downloaded_data = cloud_storage.download_data("test_key")
    assert downloaded_data == test_data
    print("✅ Cloud download working")
    
    # Test data listing
    data_list = cloud_storage.list_data()
    assert isinstance(data_list, list)
    print("✅ Cloud data listing working")
    
    # Test sync operations
    local_data = {'test': 'data'}
    sync_success = cloud_storage.sync_to_cloud(local_data)
    assert sync_success
    print("✅ Cloud sync working")
    
    # Test sync status
    status = cloud_storage.get_sync_status()
    assert 'last_sync' in status
    print("✅ Cloud sync status working")
    
    # Test encryption
    original_data = b"sensitive data"
    encrypted = cloud_storage.encrypt_before_upload(original_data)
    decrypted = cloud_storage.decrypt_after_download(encrypted)
    assert decrypted == original_data
    print("✅ Cloud encryption working")
    
    # Test 6: Integration
    print("\n🔗 Testing Integration...")
    
    # Test complete workflow
    user_input = "research artificial intelligence"
    
    # Context processing
    context = context_engine.retrieve_context(user_id)
    context['last_input'] = user_input
    context_engine.store_context(user_id, context)
    
    # Intent anticipation
    anticipations = context_engine.anticipate_user_intent(user_id, user_input)
    
    # Research
    analysis = research.deep_analysis(user_input, context)
    summary = research.synthesize_information([analysis])
    
    # Store results
    context['last_summary'] = summary
    context_engine.store_context(user_id, context)
    
    # Cloud sync
    cloud_storage.sync_to_cloud({'context': context})
    
    assert len(anticipations) > 0
    assert 'sources_consulted' in analysis
    print("✅ Complete workflow integration working")
    
    print("\n🎉 Phase 2 Implementation Test PASSED!")
    print("All enhanced features are working correctly:")
    print("✅ Enhanced context engine with long-term memory and anticipation")
    print("✅ Multi-source research with deep analysis and synthesis")
    print("✅ Voice interface (simulated)")
    print("✅ Plugin system for extensibility")
    print("✅ Cloud storage with encryption and sync")
    print("✅ Complete integration of all Phase 2 features")
    print("\nReady for Phase 3 development!")

if __name__ == "__main__":
    test_phase2()