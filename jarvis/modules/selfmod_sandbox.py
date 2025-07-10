from jarvis.interfaces.selfmod import SelfModificationInterface
import datetime

class SandboxSelfMod(SelfModificationInterface):
    LOG_FILE = 'selfmod_audit.log'

    def propose_change(self, diff: str) -> bool:
        # In Phase 1, just log the proposal
        self.log_change(f"PROPOSE: {diff}")
        return True

    def apply_change(self, diff: str) -> bool:
        # In Phase 1, just log the application
        self.log_change(f"APPLY: {diff}")
        return True

    def rollback(self) -> bool:
        # Placeholder for rollback logic
        self.log_change("ROLLBACK requested.")
        return True

    def log_change(self, diff: str) -> None:
        # Log all changes with timestamp for auditability
        with open(self.LOG_FILE, 'a') as f:
            f.write(f"{datetime.datetime.now().isoformat()} | {diff}\n")