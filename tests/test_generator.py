import pytest
from app.generator import DockerfileGenerator, generate_dockerfile
from app.llm_client import OllamaClientError
from app.prompt_templates import (
    SUPPORTED_LANGUAGES,
    build_prompt,
    load_template,
)

@pytest.fixture
def mock_llm_client(mocker):
    """Create a mocked LLM client without connecting to Ollama."""
    client = mocker.Mock()
    client.generate.return_value = (
        "FROM python:3.11-slim\n"
        "WORKDIR /app\n"
        "COPY . .\n"
        'CMD ["python", "main.py"]'
    )
    return client

@pytest.fixture
def generator(mock_llm_client):
    """Create a generator with a mocked LLM client."""
    return DockerfileGenerator(llm_client=mock_llm_client)

class TestPromptTemplates:
    """Tests for loading templates and building prompts."""
    @pytest.mark.parametrize(
        "language",
        ["python", "nodejs", "java"],
    )