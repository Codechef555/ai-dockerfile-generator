import re
from app.llm_client import LLMClient
from app.prompt_templates import build_prompt

class DockerfileGenerator:
    """Generate Dockerfile content for supported programming languages."""
    
    def __init__(self, llm_client: LLMClient | None = None) -> None:
        """Initialize the generator with an optional LLM client.

        Args:
            llm_client: An existing Ollama client wrapper. If omitted,
                a default LLMClient instance is created.
        """
        self.llm_client = llm_client or LLMClient()