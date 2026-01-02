"""
Unit tests for TaskService business logic.

Tests the service layer independently with mocked repository.
"""

import pytest
from app.models import Task, TaskStatus
from app.repository import TaskRepository
from app.service import TaskService
from app.exceptions import ValidationError, TaskNotFoundError


class TestValidation:
    """Tests for input validation."""

    def test_validate_title_valid(self) -> None:
        """Test validating a valid title."""
        service = TaskService(TaskRepository())
        result = service.validate_title("Buy groceries")
        assert result == "Buy groceries"

    def test_validate_title_empty_raises_error(self) -> None:
        """Test that empty title raises ValidationError."""
        service = TaskService(TaskRepository())
        with pytest.raises(ValidationError, match="cannot be empty"):
            service.validate_title("")

    def test_validate_title_whitespace_only_raises_error(self) -> None:
        """Test that whitespace-only title raises ValidationError."""
        service = TaskService(TaskRepository())
        with pytest.raises(ValidationError, match="cannot be empty"):
            service.validate_title("   ")

    def test_validate_title_too_long_raises_error(self) -> None:
        """Test that title > 200 chars raises ValidationError."""
        service = TaskService(TaskRepository())
        long_title = "x" * 201
        with pytest.raises(ValidationError, match="exceeds 200"):
            service.validate_title(long_title)

    def test_validate_title_trims_whitespace(self) -> None:
        """Test that title is trimmed."""
        service = TaskService(TaskRepository())
        result = service.validate_title("  Buy groceries  ")
        assert result == "Buy groceries"

    def test_validate_description_valid(self) -> None:
        """Test validating a valid description."""
        service = TaskService(TaskRepository())
        result = service.validate_description("Milk, eggs, bread")
        assert result == "Milk, eggs, bread"

    def test_validate_description_empty(self) -> None:
        """Test that empty description is valid."""
        service = TaskService(TaskRepository())
        result = service.validate_description("")
        assert result == ""

    def test_validate_description_too_long_raises_error(self) -> None:
        """Test that description > 500 chars raises ValidationError."""
        service = TaskService(TaskRepository())
        long_desc = "x" * 501
        with pytest.raises(ValidationError, match="exceeds 500"):
            service.validate_description(long_desc)

    def test_validate_task_id_exists(self) -> None:
        """Test validating an existing task ID."""
        repo = TaskRepository()
        task = Task(task_id=1, title="Test")
        repo.add_task(task)
        service = TaskService(repo)

        # Should not raise
        service.validate_task_id(1)

    def test_validate_task_id_not_found_raises_error(self) -> None:
        """Test that non-existent task ID raises TaskNotFoundError."""
        service = TaskService(TaskRepository())
        with pytest.raises(TaskNotFoundError, match="not found"):
            service.validate_task_id(99)


class TestAddTask:
    """Tests for adding tasks."""

    def test_add_task_with_title_only(self) -> None:
        """Test adding task with title only."""
        service = TaskService(TaskRepository())
        task = service.add_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE

    def test_add_task_with_title_and_description(self) -> None:
        """Test adding task with title and description."""
        service = TaskService(TaskRepository())
        task = service.add_task("Buy groceries", "Milk, eggs, bread")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"

    def test_add_multiple_tasks_increments_id(self) -> None:
        """Test that multiple tasks get sequential IDs."""
        service = TaskService(TaskRepository())
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_empty_title_raises_error(self) -> None:
        """Test that empty title raises ValidationError."""
        service = TaskService(TaskRepository())
        with pytest.raises(ValidationError, match="cannot be empty"):
            service.add_task("")

    def test_add_task_task_accessible_immediately(self) -> None:
        """Test that added task is immediately accessible."""
        service = TaskService(TaskRepository())
        task = service.add_task("Test")

        retrieved = service.get_task(task.id)
        assert retrieved == task


class TestGetTask:
    """Tests for retrieving tasks."""

    def test_get_task_existing(self) -> None:
        """Test getting an existing task."""
        service = TaskService(TaskRepository())
        added = service.add_task("Test")
        retrieved = service.get_task(added.id)

        assert retrieved == added

    def test_get_task_nonexistent_raises_error(self) -> None:
        """Test that getting non-existent task raises TaskNotFoundError."""
        service = TaskService(TaskRepository())
        with pytest.raises(TaskNotFoundError):
            service.get_task(99)

    def test_get_all_tasks_empty(self) -> None:
        """Test get_all_tasks on empty service."""
        service = TaskService(TaskRepository())
        assert service.get_all_tasks() == []

    def test_get_all_tasks_multiple(self) -> None:
        """Test get_all_tasks returns all tasks sorted by ID."""
        service = TaskService(TaskRepository())
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 3
        assert [t.id for t in all_tasks] == [1, 2, 3]


class TestUpdateTask:
    """Tests for updating tasks."""

    def test_update_title_only(self) -> None:
        """Test updating title only."""
        service = TaskService(TaskRepository())
        task = service.add_task("Original")

        updated, was_changed = service.update_task(task.id, new_title="Updated")

        assert was_changed is True
        assert updated.title == "Updated"
        assert updated.status == TaskStatus.INCOMPLETE

    def test_update_description_only(self) -> None:
        """Test updating description only."""
        service = TaskService(TaskRepository())
        task = service.add_task("Task", "Original")

        updated, was_changed = service.update_task(task.id, new_description="Updated")

        assert was_changed is True
        assert updated.description == "Updated"
        assert updated.title == "Task"

    def test_update_both_fields(self) -> None:
        """Test updating both title and description."""
        service = TaskService(TaskRepository())
        task = service.add_task("Original", "Original")

        updated, was_changed = service.update_task(
            task.id, new_title="New", new_description="Desc"
        )

        assert was_changed is True
        assert updated.title == "New"
        assert updated.description == "Desc"

    def test_update_no_changes(self) -> None:
        """Test updating with no actual changes."""
        service = TaskService(TaskRepository())
        task = service.add_task("Task")

        updated, was_changed = service.update_task(task.id, new_title="Task")

        assert was_changed is False

    def test_update_preserves_status(self) -> None:
        """Test that update preserves task status."""
        service = TaskService(TaskRepository())
        task = service.add_task("Task")
        service.mark_complete(task.id)

        updated, _ = service.update_task(task.id, new_title="Updated")

        assert updated.is_complete()

    def test_update_nonexistent_task_raises_error(self) -> None:
        """Test that updating non-existent task raises TaskNotFoundError."""
        service = TaskService(TaskRepository())
        with pytest.raises(TaskNotFoundError):
            service.update_task(99, new_title="New")

    def test_update_with_invalid_title_raises_error(self) -> None:
        """Test that invalid title raises ValidationError."""
        service = TaskService(TaskRepository())
        task = service.add_task("Task")
        with pytest.raises(ValidationError):
            service.update_task(task.id, new_title="")


class TestDeleteTask:
    """Tests for deleting tasks."""

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        service = TaskService(TaskRepository())
        task = service.add_task("Test")

        deleted = service.delete_task(task.id)

        assert deleted == task
        assert len(service.get_all_tasks()) == 0

    def test_delete_nonexistent_task_raises_error(self) -> None:
        """Test that deleting non-existent task raises TaskNotFoundError."""
        service = TaskService(TaskRepository())
        with pytest.raises(TaskNotFoundError):
            service.delete_task(99)

    def test_delete_returns_deleted_task(self) -> None:
        """Test that delete_task returns the deleted task."""
        service = TaskService(TaskRepository())
        added = service.add_task("Test")
        deleted = service.delete_task(added.id)

        assert deleted == added
        assert deleted.title == "Test"


class TestStatusOperations:
    """Tests for status transitions."""

    def test_mark_complete(self) -> None:
        """Test marking task as complete."""
        service = TaskService(TaskRepository())
        task = service.add_task("Test")

        completed = service.mark_complete(task.id)

        assert completed.is_complete()

    def test_mark_complete_already_complete_raises_error(self) -> None:
        """Test that marking already-complete as complete raises error."""
        service = TaskService(TaskRepository())
        task = service.add_task("Test")
        service.mark_complete(task.id)

        with pytest.raises(ValidationError, match="already complete"):
            service.mark_complete(task.id)

    def test_mark_incomplete(self) -> None:
        """Test marking task as incomplete."""
        service = TaskService(TaskRepository())
        task = service.add_task("Test", status=TaskStatus.COMPLETE)

        incomplete = service.mark_incomplete(task.id)

        assert not incomplete.is_complete()

    def test_mark_incomplete_already_incomplete_raises_error(self) -> None:
        """Test that marking already-incomplete as incomplete raises error."""
        service = TaskService(TaskRepository())
        task = service.add_task("Test")

        with pytest.raises(ValidationError, match="already incomplete"):
            service.mark_incomplete(task.id)

    def test_mark_nonexistent_complete_raises_error(self) -> None:
        """Test that marking non-existent task complete raises error."""
        service = TaskService(TaskRepository())
        with pytest.raises(TaskNotFoundError):
            service.mark_complete(99)

    def test_mark_nonexistent_incomplete_raises_error(self) -> None:
        """Test that marking non-existent task incomplete raises error."""
        service = TaskService(TaskRepository())
        with pytest.raises(TaskNotFoundError):
            service.mark_incomplete(99)

    def test_status_toggle_preserves_title(self) -> None:
        """Test that status toggle preserves title."""
        service = TaskService(TaskRepository())
        task = service.add_task("Original Title")

        service.mark_complete(task.id)
        completed = service.get_task(task.id)

        assert completed.title == "Original Title"

    def test_status_toggle_preserves_description(self) -> None:
        """Test that status toggle preserves description."""
        service = TaskService(TaskRepository())
        task = service.add_task("Task", "Original Desc")

        service.mark_complete(task.id)
        completed = service.get_task(task.id)

        assert completed.description == "Original Desc"


class TestStatistics:
    """Tests for task statistics."""

    def test_statistics_empty(self) -> None:
        """Test statistics on empty service."""
        service = TaskService(TaskRepository())
        total, completed, remaining = service.get_statistics()

        assert total == 0
        assert completed == 0
        assert remaining == 0

    def test_statistics_all_incomplete(self) -> None:
        """Test statistics with all incomplete tasks."""
        service = TaskService(TaskRepository())
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        total, completed, remaining = service.get_statistics()

        assert total == 3
        assert completed == 0
        assert remaining == 3

    def test_statistics_mixed(self) -> None:
        """Test statistics with mixed complete/incomplete."""
        service = TaskService(TaskRepository())
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        service.mark_complete(task1.id)
        service.mark_complete(task3.id)

        total, completed, remaining = service.get_statistics()

        assert total == 3
        assert completed == 2
        assert remaining == 1
