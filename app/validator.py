import re
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    """Store the results of Dockerfile validation."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    passed_checks: list[str] = field(default_factory=list)

class DockerfileValidator:
    