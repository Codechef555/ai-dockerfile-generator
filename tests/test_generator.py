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
        """Unsupported languages should produce a clear error."""
        with pytest.raises(ValueError, match="Unsupported language"):
            load_template("ruby")
    
    @pytest.mark.parametrize(
        "description",
        ["", "   ", "\n\t"],
    )
    def test_empty_description_raises_error(self, description):
        """Empty project descriptions should be rejected."""
        with pytest.raises(
            ValueError,
            match="Project description cannot be empty",
        ):
            build_prompt("python", description)
    
    def test_non_string_description_raises_error(self):
        """Project descriptions must be strings."""
        with pytest.raises(
            ValueError,
            match="Project description cannot be empty",
        ):
            build_prompt("python", None)
    
    def test_missing_template_file_raises_error(self, mocker):
        """A missing template should raise FileNotFoundError."""
        mocker.patch(
            "app.prompt_templates.TEMPLATES_DIR",
            mocker.Mock(
                __truediv__=mocker.Mock(
                    return_value=mocker.Mock(
                        read_text=mocker.Mock(
                            side_effect=FileNotFoundError(
                                "Template not found"
                            )
                        )
                    )
                )
            ),
        )
        with pytest.raises(FileNotFoundError):
            load_template("python")

class TestDockerfileGenerator:
    """Tests for Dockerfile generation."""
    def test_generator_initialization(self, mock_llm_client):
        """The supplied LLM client should be stored."""
        instance = DockerfileGenerator(llm_client=mock_llm_client)
        assert instance.llm_client is mock_llm_client

    @pytest.mark.parametrize(
        "language",
        ["python", "nodejs", "java"],
    )
    def test_generate_supported_languages(self, generator, mock_llm_client, language):
        """Generation should work for every supported language."""
        result = generator.generate(language, "A simple REST API.",)
        assert result.startswith("FROM python:3.11-slim")
        assert "WORKDIR /app" in result

        mock_llm_client.generate.assert_called_once()

    def test_generate_builds_prompt(self, mock_llm_client, mocker):
        """The generator should pass a built prompt to the LLM."""
        build_prompt_mock = mocker.patch(
            "app.generator.build_prompt",
            return_value="Test prompt",
        )

        instance = DockerfileGenerator(llm_client=mock_llm_client)
        instance.generate("python", "A test application.")

        build_prompt_mock.assert_called_once_with(
            "python",
            "A test application.",
        )

        mock_llm_client.generate.assert_called_once_with("Test prompt")

    def test_generate_removes_markdown_fences(self, mock_llm_client):
        """Markdown fences should be removed from model output."""
        mock_llm_client.generate.return_value = (
            "```dockerfile\n"
            "FROM python:3.11-slim\n"
            'CMD ["python", "main.py"]\n'
            "```"
        )

        instance = DockerfileGenerator(llm_client=mock_llm_client)
        result = instance.generate("python", "A simple API.")

        assert result.startswith("FROM")
        assert "```" not in result

    def test_generate_preserves_valid_dockerfile_content(self, mock_llm_client):
        """Valid Dockerfile instructions should remain unchanged."""
        dockerfile = (
            "FROM python:3.11-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt .\n"
            "RUN pip install -r requirements.txt\n"
            'CMD ["python", "main.py"]'
        )

        mock_llm_client.generate.return_value = dockerfile

        instance = DockerfileGenerator(llm_client=mock_llm_client)
        result = instance.generate("python", "A Python API.")

        assert result == dockerfile

    def test_empty_llm_response_raises_error(self, mock_llm_client):
        """Empty model output should be rejected."""
        mock_llm_client.generate.return_value = "   "
        instance = DockerfileGenerator(llm_client=mock_llm_client)
        with pytest.raises(
            ValueError,
            match="empty Dockerfile",
        ):
            instance.generate("python", "A test API.")

    def test_unsupported_language_raises_error(self, generator):
        """Unsupported languages should not reach the LLM."""
        with pytest.raises(ValueError, match="Unsupported language"):
            generator.generate("ruby", "A Ruby application.")
