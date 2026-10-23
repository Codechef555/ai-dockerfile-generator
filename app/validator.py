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
    """Perform basic static validation of Dockerfile content."""
    # Instructions commonly used in Dockerfiles.
    INSTRUCTION_PATTERN = re.compile(
        r"^\s*(FROM|RUN|CMD|LABEL|EXPOSE|ENV|ADD|COPY|"
        r"ENTRYPOINT|VOLUME|USER|WORKDIR|ARG|SHELL|"
        r"HEALTHCHECK|STOPSIGNAL|ONBUILD)\s+",
        re.IGNORECASE,
    )
    FROM_PATTERN = re.compile(
        r"^\s*FROM\s+(?:--platform=\S+\s+)?\S+",
        re.IGNORECASE | re.MULTILINE,
    )
    def validate(self, dockerfile: str) -> ValidationResult:
        """Validate Dockerfile content.

        Args:
            dockerfile: Dockerfile content to inspect.

        Returns:
            A ValidationResult containing errors, warnings, and passed checks.

        Raises:
            ValueError: If the Dockerfile content is not a string.
        """
        if not isinstance(dockerfile, str):
            raise ValueError("Dockerfile content must be a string.")

        if not dockerfile.strip():
            return ValidationResult(
                is_valid=False,
                errors=["Dockerfile content cannot be empty."],
            )
