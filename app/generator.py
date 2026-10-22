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
    
    def generate(self, language: str, project_description: str) -> str:
        """Generate a Dockerfile for the specified project.

        Args:
            language: Target language: python, nodejs, or java.
            project_description: Description of the application.

        Returns:
            Cleaned Dockerfile content.

        Raises:
            ValueError: If the language or description is invalid.
            FileNotFoundError: If the language template is missing.
            OllamaClientError: If Ollama generation fails.
        """
        prompts = build_prompt(language, project_description)
        response = self.llm_client.generate(prompt)
        dockerfile = self._clean_output(response)

        if not dockerfile:
            raise ValueError("The LLM returned an empty Dockerfile after cleaning.")
        return dockerfile

    @staticmethod
    def _clean_output(response: str) -> str:
        """Remove surrounding Markdown fences and unwanted whitespace.

        Args:
            response: Raw text returned by the LLM.

        Returns:
            Cleaned Dockerfile text.
        """
        if not isinstance(response, str):
            raise ValueError("LLM response must be a string.")
        output = response.strip()
        # Remove an opening Markdown fence, optionally labelled Dockerfile.
        output = re.sub(
            r"\A```(?:dockerfile|docker)?[ \t]*\r?\n",
            "",
            output,
            count=1,
            flags=re.IGNORECASE,
        )
        # Remove a closing Markdown fence.
        output = re.sub(
            r"\r?\n?[ \t]*```[ \t]*\Z",
            "",
            output,
            count=1,
        )

        return output.strip()