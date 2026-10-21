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
        try:
            response = self.client.list()
            models = response.models

            available_models = {
                model.model or model.name
                for model in models
            }

            if self.model not in available_models:
                raise OllamaClientError(
                    f"Model '{self.model}' is not installed. "
                    f"Run: ollama pull {self.model}"
                )

            return True

        except OllamaClientError:
            raise
        except Exception as exc:
            raise OllamaClientError(
                f"Failed to check Ollama model availability: {exc}"
            ) from exc
    
    def generate(self, prompt: str) -> str:
        """Generate text using the configured local model.

        Args:
            prompt: Complete prompt to send to the model.

        Returns:
            The generated text.

        Raises:
            ValueError: If the prompt is empty.
            OllamaClientError: If generation fails or returns empty output.
        """

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False,
            )

            generated_text = response.response.strip()

            if not generated_text:
                raise OllamaClientError(
                    "Ollama returned an empty response."
                )

            return generated_text

        except OllamaClientError:
            raise
        except ResponseError as exc:
            raise OllamaClientError(
                f"Ollama model error: {exc}"
            ) from exc
        except Exception as exc:
            raise OllamaClientError(
                f"Failed to generate text using Ollama: {exc}"
            ) from exc