"""
JARVIS Next-Gen AI Personal Assistant
Main entry point for Phase 1 prototype.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jarvis.modules.interaction_cli import CLIInteraction
from jarvis.modules.context_memory import MemoryContextEngine
from jarvis.modules.research_web import WebResearch
from jarvis.modules.selfmod_sandbox import SandboxSelfMod
from jarvis.modules.storage_encrypted import EncryptedStorage

USER_ID = 'default_user'  # For Phase 1, single user

def main():
    # Initialize core modules
    interaction = CLIInteraction()
    context_engine = MemoryContextEngine()
    research = WebResearch()
    selfmod = SandboxSelfMod()
    storage = EncryptedStorage()

    interaction.send_message("Welcome to JARVIS AI Assistant (Phase 1 Prototype)")
    while True:
        user_input = interaction.get_user_input()
        if user_input.lower() in {"exit", "quit"}:
            interaction.send_message("Goodbye!")
            break
        # Store user input in context
        context = context_engine.retrieve_context(USER_ID)
        context['last_input'] = user_input
        context_engine.store_context(USER_ID, context)
        # Perform research
        results = research.search(user_input)
        summary = research.summarize(results)
        # Store summary in context
        context['last_summary'] = summary
        context_engine.store_context(USER_ID, context)
        # Respond to user
        interaction.send_message(summary)

if __name__ == "__main__":
    main()