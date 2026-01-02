"""
Custom exception classes for the Todo application.

These exceptions are raised by the service layer and caught by the CLI layer
to provide user-friendly error messages.
"""


class TodoAppException(Exception):
    """Base exception for the Todo application."""

    pass


class ValidationError(TodoAppException):
    """Raised when input validation fails."""

    pass


class TaskNotFoundError(TodoAppException):
    """Raised when a task ID doesn't exist."""

    pass
