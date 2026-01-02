"""
Repository layer: In-memory task storage.

This module manages task storage using a Python dictionary.
The repository handles task persistence in memory and sequential ID generation.
"""

from typing import Dict, List, Optional

try:
    from app.models import Task
except ModuleNotFoundError:
    from models import Task


class TaskRepository:
    """
    In-memory task repository using Python dictionary storage.

    Manages task storage and ID generation. Implements the repository pattern
    to abstract storage from business logic, enabling easy migration to
    persistent storage in future phases.
    """

    def __init__(self) -> None:
        """Initialize empty task repository."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, task: Task) -> Task:
        """
        Add a task to storage.

        Args:
            task: Task instance to add

        Returns:
            The added task
        """
        self._tasks[task.id] = task
        self._next_id = max(self._next_id, task.id + 1)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task instance if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks sorted by ID in ascending order.

        Returns:
            List of all tasks sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task ID to delete

        Returns:
            True if task was deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def task_exists(self, task_id: int) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: Task ID to check

        Returns:
            True if task exists, False otherwise
        """
        return task_id in self._tasks

    def get_next_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            Next ID to be assigned (sequential)
        """
        return self._next_id

    def clear(self) -> None:
        """Clear all tasks and reset ID counter to 1."""
        self._tasks.clear()
        self._next_id = 1
