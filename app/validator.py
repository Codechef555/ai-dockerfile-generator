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
        
        # Warn when the base image uses the mutable latest tag.
        if re.search(
            r"^\s*FROM\s+(?:--platform=\S+\s+)?\S+:latest(?:\s|$)",
            dockerfile,
            re.IGNORECASE | re.MULTILINE,
        ):
            warnings.append(
                "A base image uses the 'latest' tag. "
                "Consider pinning a specific version for reproducibility."
            )
        # Check whether files are copied into the image.
        if re.search(r"^\s*(COPY|ADD)\s+", dockerfile, re.IGNORECASE | re.MULTILINE):
            passed_checks.append("COPY or ADD instruction found.")
        else:
            warnings.append(
                "No COPY or ADD instruction found. "
                "Verify whether application files need to be copied."
            )
        
        # Check whether the container specifies a working directory.
        if re.search(r"^\s*WORKDIR\s+\S+", dockerfile, re.IGNORECASE | re.MULTILINE):
            passed_checks.append("WORKDIR instruction found.")
        else:
            warnings.append(
                "No WORKDIR instruction found. "
                "Consider setting an explicit application directory."
            )
        # Check for a non-root USER instruction.
        user_matches = re.findall(
            r"^\s*USER\s+(\S+)",
            dockerfile,
            re.IGNORECASE | re.MULTILINE,
        )

        if user_matches:
            final_user = user_matches[-1].lower()

            if final_user in {"root", "0"}:
                warnings.append(
                    "The final USER instruction runs as root. "
                    "Consider using a non-root user."
                )
            else:
                passed_checks.append("A non-root final USER is specified.")
        else:
            warnings.append(
                "No USER instruction found. The container may run as root "
                "unless the base image specifies another user."
            )
        # Flag common risky shell execution patterns.
        unsafe_patterns = {
            r"\bcurl\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba)?sh\b":
                "Downloading and executing a script directly with curl "
                "can be unsafe.",
            r"\bwget\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba)?sh\b":
                "Downloading and executing a script directly with wget "
                "can be unsafe.",
            r"\bchmod\s+(?:-R\s+)?777\b":
                "chmod 777 grants broad permissions. Use more restrictive "
                "permissions where possible.",
            r"^\s*RUN\s+.*\bsudo\b":
                "sudo inside a Docker build is often unnecessary and "
                "may indicate an avoidable privilege escalation.",
        }

        for pattern, message in unsafe_patterns.items():
            if re.search(
                pattern,
                dockerfile,
                re.IGNORECASE | re.MULTILINE,
            ):
                warnings.append(message)
        
        # Flag environment variables or build arguments that may contain secrets.
        secret_pattern = re.compile(
            r"^\s*(?:ARG|ENV)\s+"
            r"([A-Za-z_][A-Za-z0-9_]*)"
            r"(?:\s*=\s*|\s+)(.*)$",
            re.IGNORECASE | re.MULTILINE,
        )
        
        sensitive_names = {
            "password",
            "passwd",
            "secret",
            "api_key",
            "apikey",
            "access_token",
            "auth_token",
            "private_key",
        }

        for match in secret_pattern.finditer(dockerfile):
            variable_name = match.group(1).lower()
            variable_value = match.group(2).strip()

            if (
                any(name in variable_name for name in sensitive_names)
                and variable_value
                and variable_value not in {"", '""', "''"}
            ):
                warnings.append(
                    f"Potential secret in ARG or ENV variable "
                    f"'{match.group(1)}'. Use a safer secrets-management "
                    "approach instead of embedding credentials."
                )
        # A HEALTHCHECK is useful for many services but not every container.
        if re.search(
            r"^\s*HEALTHCHECK\s+",
            dockerfile,
            re.IGNORECASE | re.MULTILINE,
        ):
            passed_checks.append("HEALTHCHECK instruction found.")
        else:
            warnings.append(
                "No HEALTHCHECK instruction found. "
                "Consider adding one if container health monitoring is needed."
            )

        return ValidationResult(
            is_valid=not errors,
            errors=errors,
            warnings=warnings,
            passed_checks=passed_checks,
        )
        
def validate_dockerfile(dockerfile: str) -> ValidationResult:
    """Convenience function to validate Dockerfile content.

    Args:
        dockerfile: Dockerfile content to inspect.

    Returns:
        A ValidationResult containing the validation outcome.
    """
    validator = DockerfileValidator()
    return validator.validate(dockerfile)