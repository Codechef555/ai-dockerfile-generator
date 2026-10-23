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
        errors: list[str] = []
        warnings: list[str] = []
        passed_checks: list[str] = []

        lines = dockerfile.splitlines()
        # Remove blank lines and comments for basic instruction checks.
        meaningful_lines = [
            line.strip()
            for line in lines
            if line.strip() and not line.lstrip().startswith("#")
        ]

        if not meaningful_lines:
            errors.append("Dockerfile contains no executable instructions.")
            return ValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                passed_checks=passed_checks,
            )

        # Check for a valid base image instruction.
        if self.FROM_PATTERN.search(dockerfile):
            passed_checks.append("Base image instruction (FROM) found.")
        else:
            errors.append(
                "Missing or invalid FROM instruction specifying a base image."
            )
        # Check whether the file contains recognizable Docker instructions.
        if any(
            self.INSTRUCTION_PATTERN.match(line)
            for line in meaningful_lines
        ):
            passed_checks.append("Recognizable Docker instructions found.")
        else:
            errors.append("No recognizable Docker instructions were found.")

        # Detect Markdown fences accidentally included in the output.
        if "```" in dockerfile:
            errors.append(
                "Markdown code fences found. Remove them from the Dockerfile."
            )
        else:
            passed_checks.append("No Markdown code fences found.")