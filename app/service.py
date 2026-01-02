"""
Service layer: Task business logic and validation.

This module implements the TaskService class which coordinates task operations
between the domain layer and CLI layer. All validation and business logic
happens here, raising typed exceptions for the CLI layer to handle.
"""

from typing import List, Tuple, Optional

try:
    from app.models import Task, TaskStatus
    from app.repository import TaskRepository
    from app.exceptions import TaskNotFoundError, ValidationError
except ModuleNotFoundError:
    from models import Task, TaskStatus
    from repository import TaskRepository
    from exceptions import TaskNotFoundError, ValidationError


class TaskService:
    """
    Task service layer.

    Coordinates task operations between domain and CLI layers.
    Performs business logic, validation, and state management.
    Raises typed exceptions for CLI error handling.
    """

    def __init__(self, repository: TaskRepository) -> None:
        """
        Initialize service with repository.

        Args:
            repository: TaskRepository instance for task storage
        """
        self.repo = repository

    # --- Validation Methods ---

    def validate_title(self, title: str) -> str:
        """
        Validate and normalize task title.

        Args:
            title: Raw title input

        Returns:
            Validated and trimmed title

        Raises:
            ValidationError: If title is invalid (empty, too long, etc.)
        """
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")

        trimmed = title.strip()

        if len(trimmed) > 200:
            raise ValidationError("Task title exceeds 200 characters")

        return trimmed

    def validate_description(self, description: str) -> str:
        """
        Validate and normalize task description.

        Args:
            description: Raw description input

        Returns:
            Validated description (empty string if not provided)

        Raises:
            ValidationError: If description exceeds max length
        """
        if not description:
            return ""

        trimmed = description.strip()

        if len(trimmed) > 500:
            raise ValidationError("Description exceeds 500 characters")

        return trimmed

    def validate_task_id(self, task_id: int) -> None:
        """
        Validate that task ID exists.

        Args:
            task_id: Task ID to validate

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if not self.repo.task_exists(task_id):
            raise TaskNotFoundError(f"Task ID {task_id} not found")

    # --- CRUD Operations ---

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create and add a new task.

        Args:
            title: Task title (required)
            description: Task description (optional)

        Returns:
            Created Task instance

        Raises:
            ValidationError: If title or description invalid
        """
        validated_title = self.validate_title(title)
        validated_description = self.validate_description(description)

        task = Task(
            task_id=self.repo.get_next_id(),
            title=validated_title,
            description=validated_description,
        )

        return self.repo.add_task(task)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks sorted by ID.

        Returns:
            List of all tasks in ascending ID order
        """
        return self.repo.get_all_tasks()

    def get_task(self, task_id: int) -> Task:
        """
        Get a task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task instance

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        self.validate_task_id(task_id)
        return self.repo.get_task(task_id)

    def update_task(
        self,
        task_id: int,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Tuple[Task, bool]:
        """
        Update a task's title and/or description.

        Args:
            task_id: Task ID to update
            new_title: New title (None = no change)
            new_description: New description (None = no change)

        Returns:
            Tuple of (updated Task, was_changed boolean)

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If new values invalid
        """
        self.validate_task_id(task_id)
        task = self.repo.get_task(task_id)

        was_changed = False

        if new_title is not None:
            validated_title = self.validate_title(new_title)
            if validated_title != task.title:
                task.update_title(validated_title)
                was_changed = True

        if new_description is not None:
            validated_description = self.validate_description(new_description)
            if validated_description != task.description:
                task.update_description(validated_description)
                was_changed = True

        return task, was_changed

    def delete_task(self, task_id: int) -> Task:
        """
        Delete a task.

        Args:
            task_id: Task ID to delete

        Returns:
            Deleted Task (for confirmation display)

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        self.validate_task_id(task_id)
        task = self.repo.get_task(task_id)
        self.repo.delete_task(task_id)
        return task

    # --- Status Operations ---

    def mark_complete(self, task_id: int) -> Task:
        """
        Mark a task as complete.

        Args:
            task_id: Task ID to mark complete

        Returns:
            Updated Task

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If already complete
        """
        self.validate_task_id(task_id)
        task = self.repo.get_task(task_id)

        if task.is_complete():
            raise ValidationError("Task is already complete")

        task.mark_complete()
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """
        Mark a task as incomplete.

        Args:
            task_id: Task ID to mark incomplete

        Returns:
            Updated Task

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If already incomplete
        """
        self.validate_task_id(task_id)
        task = self.repo.get_task(task_id)

        if not task.is_complete():
            raise ValidationError("Task is already incomplete")

        task.mark_incomplete()
        return task

    def get_statistics(self) -> Tuple[int, int, int]:
        """
        Get task statistics.

        Returns:
            Tuple of (total_tasks, completed_tasks, remaining_tasks)
        """
        tasks = self.get_all_tasks()
        total = len(tasks)
        completed = sum(1 for t in tasks if t.is_complete())
        remaining = total - completed
        return total, completed, remaining
