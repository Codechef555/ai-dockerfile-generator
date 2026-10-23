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