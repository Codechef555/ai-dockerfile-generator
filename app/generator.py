import re
from app.llm_client import LLMClient
from app.prompt_templates import build_prompt

class DockerfileGenerator:
    """Generate Dockerfile content for supported programming languages."""
    