import pytest
from app.generator import DockerfileGenerator, generate_dockerfile
from app.llm_client import OllamaClientError