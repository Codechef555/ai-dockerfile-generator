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
    def test_load_supported_templates(self, language):
        """Every supported language should have a readable template."""
        template = load_template(language)

        assert isinstance(template, str)
        assert template.strip()
        assert "{project_description}" in template
    
    @pytest.mark.parametrize(
        "language",
        ["python", "nodejs", "java"],
    )
    def test_build_prompt_includes_project_description(self, language):
        """The generated prompt should contain the supplied description."""
        description = "A REST API for managing products."

        prompt = build_prompt(language, description)

        assert description in prompt
        assert "{project_description}" not in prompt
    
    def test_language_is_case_insensitive(self):
        """Language names should be normalized to lowercase."""
        assert load_template("PYTHON") == load_template("python")
    
    def test_language_whitespace_is_accepted(self):
        """Leading and trailing whitespace should be ignored."""
        assert load_template(" python ") == load_template("python")
    
    def test_unsupported_language_raises_error(self):