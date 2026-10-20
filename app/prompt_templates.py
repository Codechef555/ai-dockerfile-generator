from pathlib import Path

# Resolve the project root independently of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"

SUPPORTED_LANGUAGES = {
    "python": "python.txt",
    "nodejs": "nodejs.txt",
    "java": "java.txt"
}