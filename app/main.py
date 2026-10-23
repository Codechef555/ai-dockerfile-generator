import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax

from app.generator import DockerfileGenerator
from app.llm_client import LLMClient, OllamaClientError
from app.validator import DockerfileValidator, ValidationResult

console = Console()
SUPPORTED_LANGUAGES = ("python", "nodejs", "java")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "generated"

def display_validation_result(result: ValidationResult) -> None:
    """Display Dockerfile validation results in the terminal.

    Args:
        result: Result returned by DockerfileValidator.
    """
    if result.passed_checks:
        console.print("\n[bold green]Passed Checks[/bold green]")

        for check in result.passed_checks:
            console.print(f"  [green]+[/green] {check}")

    if result.warnings:
        console.print("\n[bold yellow]Warnings[/bold yellow]")

        for warning in result.warnings:
            console.print(f"  [yellow]![/yellow] {warning}")
    if result.errors:
        console.print("\n[bold red]Validation Errors[/bold red]")

        for error in result.errors:
            console.print(f"  [red]x[/red] {error}")
    if result.is_valid:
        console.print(
            "\n[bold green]Validation status: PASSED[/bold green]"
        )
    else:
        console.print(
            "\n[bold red]Validation status: FAILED[/bold red]"
        )
def save_dockerfile(
    content: str,
    output_path: str | Path,
) -> Path:
    """Save Dockerfile content to disk.

    Args:
        content: Generated Dockerfile content.
        output_path: Destination file path.

    Returns:
        The resolved path of the saved Dockerfile.

    Raises:
        ValueError: If the content is empty or the path is invalid.
        OSError: If the file cannot be written.
    """
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Cannot save an empty Dockerfile.")

    destination = Path(output_path).expanduser()

    if destination.exists() and destination.is_dir():
        destination = destination / "Dockerfile"

    if not destination.name:
        raise ValueError("Output path must specify a filename.")
    
    if destination.exists():
        if not destination.is_file():
            raise ValueError("Output path must refer to a file.")

        if not Confirm.ask(
            f"[yellow]{destination} already exists. Overwrite it?[/yellow]",
            default=False,
        ):
            console.print("[yellow]Save cancelled.[/yellow]")
            return destination
    
    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content.rstrip() + "\n", encoding="utf-8")

    console.print(
        f"\n[bold green]Dockerfile saved successfully:[/bold green]\n"
        f"{destination}"
    )

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Generate and validate Dockerfiles using a locally running "
            "Ollama model."
        )
    )
