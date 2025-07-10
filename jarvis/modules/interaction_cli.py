from jarvis.interfaces.interaction import UserInteractionInterface
from rich.console import Console

class CLIInteraction(UserInteractionInterface):
    def __init__(self):
        self.console = Console()

    def send_message(self, message: str) -> str:
        self.console.print(f"[bold blue]JARVIS:[/bold blue] {message}")
        return message

    def get_user_input(self) -> str:
        return self.console.input("[bold green]You:[/bold green] ")