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

    parser.add_argument(
        "--language",
        choices=SUPPORTED_LANGUAGES,
        help="Application language: python, nodejs, or java.",
    )

    parser.add_argument(
        "--description",
        help="Description of the application to containerize.",
    )

    parser.add_argument(
        "--output",
        help="Output path for the generated Dockerfile.",
    )

    parser.add_argument(
        "--model",
        help="Ollama model to use, such as llama3.2:1b.",
    )

    return parser.parse_args()

def main() -> int:
    """Run the Dockerfile generation application.

    Returns:
        Process exit code: 0 for success, nonzero for failure.
    """
    console.print(
        Panel(
            "[bold cyan]Local Dockerfile Generator[/bold cyan]\n"
            "Generate and validate Dockerfiles using local AI.",
            title="Welcome",
            border_style="cyan",
        )
    )
    args = parse_arguments()
    try:
        # Collect input interactively when arguments are not provided.
        language = args.language or Prompt.ask(
            "Select the application language",
            choices=list(SUPPORTED_LANGUAGES),
            default="python",
        )

        description = args.description or Prompt.ask(
            "Describe your application",
        )

        if not description.strip():
            console.print(
                "[bold red]Error:[/bold red] "
                "Project description cannot be empty."
            )
            return 1
         
        default_output = DEFAULT_OUTPUT_DIR / "Dockerfile"
        output_path = args.output or str(default_output)

        # Initialize the local LLM client.
        llm_client = LLMClient(model=args.model)

        console.print("\n[cyan]Checking Ollama connection...[/cyan]")
        llm_client.check_connection()
        console.print("[green]Ollama is running.[/green]")

        console.print("[cyan]Checking model availability...[/cyan]")
        llm_client.check_model()
        console.print("[green]Configured model is available.[/green]")

        # Generate Dockerfile content.
        generator = DockerfileGenerator(llm_client=llm_client)

        console.print(
            f"\n[cyan]Generating Dockerfile for {language}...[/cyan]"
        )
        
        with console.status(
            "[bold cyan]Asking the local LLM to generate a Dockerfile..."
        ):
            dockerfile_content = generator.generate(
                language=language,
                project_description=description,
            )

