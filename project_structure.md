# Project Structure & Core Interfaces (Phase 1)

## Directory Layout

```
/ (root)
|-- README.md
|-- project_structure.md
|-- jarvis/
|    |-- __init__.py
|    |-- main.py              # Entry point
|    |-- interfaces/
|    |    |-- __init__.py
|    |    |-- interaction.py  # User interaction interface
|    |    |-- context.py      # Context engine interface
|    |    |-- research.py     # Research/web search interface
|    |    |-- selfmod.py      # Self-modification interface
|    |    |-- storage.py      # Secure storage interface
|    |-- modules/
|         |-- __init__.py
|         |-- interaction_cli.py
|         |-- context_memory.py
|         |-- research_web.py
|         |-- selfmod_sandbox.py
|         |-- storage_encrypted.py
|-- tests/
|    |-- test_interaction.py
|    |-- test_context.py
|    |-- test_research.py
|    |-- test_selfmod.py
|    |-- test_storage.py
|-- requirements.txt
```

## Core Interfaces (Python, `jarvis/interfaces/`)

### 1. `interaction.py`
- `class UserInteractionInterface:`
    - `def send_message(self, message: str) -> str:`
    - `def get_user_input(self) -> str:`

### 2. `context.py`
- `class ContextEngineInterface:`
    - `def store_context(self, user_id: str, context: dict) -> None:`
    - `def retrieve_context(self, user_id: str) -> dict:`
    - `def clear_context(self, user_id: str) -> None:`

### 3. `research.py`
- `class ResearchInterface:`
    - `def search(self, query: str) -> dict:`
    - `def summarize(self, results: dict) -> str:`

### 4. `selfmod.py`
- `class SelfModificationInterface:`
    - `def propose_change(self, diff: str) -> bool:`
    - `def apply_change(self, diff: str) -> bool:`
    - `def rollback(self) -> bool:`
    - `def log_change(self, diff: str) -> None:`

### 5. `storage.py`
- `class SecureStorageInterface:`
    - `def store_data(self, key: str, data: bytes) -> None:`
    - `def retrieve_data(self, key: str) -> bytes:`
    - `def delete_data(self, key: str) -> None:`

---

## Notes
- All modules must follow these interfaces for easy extensibility and testing.
- Security and privacy are enforced at the storage and self-modification layers.
- This structure will evolve as new features are added in later phases.