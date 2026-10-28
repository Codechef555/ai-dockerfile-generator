import pytest
from app.validator import DockerfileValidator, ValidationResult, validate_dockerfile

@pytest.fixture
def validator():
    """Create a Dockerfile validator instance."""
    return DockerfileValidator()

@pytest.fixture
def valid_dockerfile():
    """Provide a basic Dockerfile for testing."""
    return (
        "FROM python:3.11-slim\n"
        "WORKDIR /app\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "COPY . .\n"
        "USER 10001\n"
        'CMD ["python", "main.py"]\n'
    )

class TestDockerfileValidator:
    """Tests for the DockerfileValidator class."""

    def test_valid_dockerfile_passes(self, validator, valid_dockerfile):
        """A structurally valid Dockerfile should pass validation."""
        result = validator.validate(valid_dockerfile)

        assert isinstance(result, ValidationResult)
        assert result.is_valid is True
        assert result.errors == []
        assert result.passed_checks
    
    def test_empty_dockerfile_fails(self, validator):
        """An empty Dockerfile should fail validation."""
        result = validator.validate("")

        assert result.is_valid is False
        assert "Dockerfile content cannot be empty." in result.errors
    
    @pytest.mark.parametrize("content", ["   ", "\n", "\t\n  "])
    def test_whitespace_only_dockerfile_fails(self, validator, content):
        """Whitespace-only content should be rejected."""
        result = validator.validate(content)

        assert result.is_valid is False
        assert result.errors

    def test_non_string_content_raises_error(self, validator):
        """Non-string content should raise ValueError."""   
        with pytest.raises(
            ValueError,
            match="Dockerfile content must be a string",
        ):
            validator.validate(None)

    def test_missing_from_instruction_fails(self, validator):
        """A Dockerfile without FROM should fail validation."""
        result = validator.validate(
            "WORKDIR /app\n"
            'CMD ["python", "main.py"]\n'
        )
        assert result.is_valid is False
        assert any("FROM" in error for error in result.errors)        