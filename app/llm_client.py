import os 
import ollama
from ollama import chat, ResponseError

DEFAULT_MODEL = "llama3.2:1b"
DEFALUT_HOST = "http://localhost:11434"

class OllamaClientError(Exception):
    """Raised when an Ollama request fails."""

class LLMClient:
    """Send prompts to a locally running Ollama model."""
    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
        timeout: float = 120.0,
    ) -> None:
        """Initialize the Ollama client.

        Args:
            model: Ollama model name. Defaults to llama3.2:1b.
            host: Ollama server URL. Defaults to localhost.
            timeout: Request timeout in seconds.
        """
        self.model = model or os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
        self.host = host or os.getenv("OLLAMA_HOST", DEFAULT_HOST)

        if not self.model.strip():
            raise ValueError("Ollama model name cannot be empty.")

        if timeout <= 0:
            raise ValueError("Timeout must be greater than zero.")

        self.timeout = timeout
        self.client = ollama.Client(
            host=self.host,
            timeout=self.timeout,
        )
    def check_connection(self) -> bool:
        """Check whether the Ollama server is reachable.

        Returns:
            True if the server responds successfully.

        Raises:
            OllamaClientError: If the server cannot be reached.
        """
        try:
            self.client.list()
            return True
        except Exception as exc:
            raise OllamaClientError(
                f"Cannot connect to Ollama at {self.host}. "
                "Ensure Ollama is installed and running."
            ) from exc
    
    def check_model(self) -> bool:
        """Check whether the configured model is available locally.

        Returns:
            True if the model is installed.

        Raises:
            OllamaClientError: If the model is unavailable or the check fails.
        """