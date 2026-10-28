import pytest
from app.validator import DockerfileValidator, ValidationResult, validate_dockerfile

@pytest.fixture
def validator():
    """Create a Dockerfile validator instance."""
    return DockerfileValidator()