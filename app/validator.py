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