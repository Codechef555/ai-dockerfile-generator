from pathlib import Path

# Resolve the project root independently of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"

SUPPORTED_LANGUAGES = {
    "python": "python.txt",
    "nodejs": "nodejs.txt",
    "java": "java.txt",
}

def load_template(language: str) -> str:
    """Load and return the template for a supported language.

    Args:
        language: Target programming language.

    Returns:
        The contents of the corresponding template file.

    Raises:
        ValueError: If the language is not supported.
        FileNotFoundError: If the template file does not exist.
        OSError: If the template cannot be read.
    """
    normalized_language = language.strip().lower()

    if normalized_language not in SUPPORTED_LANGUAGES:
        supported = ", ".join(SUPPORTED_LANGUAGES)
        raise ValueError(
            f"Unsupported language: {language!r}. "
            f"Supported languages: {supported}"
        )

    template_path = TEMPLATES_DIR / SUPPORTED_LANGUAGES[normalized_language]

    return template_path.read_text(encoding="utf-8")