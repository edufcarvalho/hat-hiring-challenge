from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    location: tuple[str, ...]
    message: str


class DomainValidationError(ValueError):
    def __init__(self, message: str, *args: object, errors: list[ValidationIssue]):
        super().__init__(message)
        self.message = message
        self.errors = errors
