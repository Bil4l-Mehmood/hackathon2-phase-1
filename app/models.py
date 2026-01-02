"""
Domain layer: Task model and status enumeration.

This module defines the Task entity and TaskStatus enum for the todo application.
Tasks are immutable in ID but mutable in title, description, and status.
"""

from enum import Enum
from datetime import datetime
from typing import Optional


class TaskStatus(Enum):
    """Task completion status enumeration."""

    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


class Task:
    """
    Task domain entity representing a single todo item.

    A Task has an immutable ID, mutable title/description/status, and a
    creation timestamp. Tasks are database-agnostic and independent of CLI.

    Attributes:
        id: Unique, immutable task ID (auto-generated, sequential)
        title: Task title, 1-200 characters (mutable)
        description: Optional task description, 0-500 chars (mutable)
        status: Task completion status: INCOMPLETE or COMPLETE (mutable)
        created_at: Creation timestamp in ISO 8601 format (immutable)
    """

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        status: TaskStatus = TaskStatus.INCOMPLETE,
        created_at: Optional[datetime] = None,
    ) -> None:
        """
        Initialize a Task.

        Args:
            task_id: Unique sequential task ID
            title: Task title (required)
            description: Task description (optional, defaults to empty string)
            status: Task status (defaults to INCOMPLETE)
            created_at: Creation timestamp (defaults to current time)
        """
        self.id: int = task_id
        self.title: str = title
        self.description: str = description
        self.status: TaskStatus = status
        self.created_at: datetime = created_at or datetime.now()

    def update_title(self, new_title: str) -> None:
        """
        Update task title.

        Args:
            new_title: New title string
        """
        self.title = new_title

    def update_description(self, new_description: str) -> None:
        """
        Update task description.

        Args:
            new_description: New description string
        """
        self.description = new_description

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.status = TaskStatus.COMPLETE

    def mark_incomplete(self) -> None:
        """Mark task as incomplete."""
        self.status = TaskStatus.INCOMPLETE

    def is_complete(self) -> bool:
        """
        Check if task is complete.

        Returns:
            True if status is COMPLETE, False otherwise
        """
        return self.status == TaskStatus.COMPLETE

    def __repr__(self) -> str:
        """String representation of task."""
        status_symbol = "✓" if self.is_complete() else "○"
        return f"[{self.id}] {status_symbol} {self.title}"
