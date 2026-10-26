import pytest
from app.generator import DockerfileGenerator, generate_dockerfile
from app.llm_client import OllamaClientError
from app.prompt_templates import (
    SUPPORTED_LANGUAGES,
    build_prompt,
    load_template,
)