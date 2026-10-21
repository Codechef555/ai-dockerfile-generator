import os 
import ollama
from ollama import chat, ResponseError

DEFAULT_MODEL = "llama3.2:1b"
DEFALUT_HOST = "http://localhost:11434"

class OllamaClientError(Exception):
    """Raised when an Ollama request fails."""
