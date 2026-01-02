"""
Unit tests for Task domain model.

Tests the Task entity and TaskStatus enum independently.
"""

import pytest
from datetime import datetime
from app.models import Task, TaskStatus


class TestTaskStatus:
    """Tests for TaskStatus enumeration."""

    def test_incomplete_value(self) -> None:
        """Test INCOMPLETE status value."""
        assert TaskStatus.INCOMPLETE.value == "incomplete"

    def test_complete_value(self) -> None:
        """Test COMPLETE status value."""
        assert TaskStatus.COMPLETE.value == "complete"

    def test_enum_comparison(self) -> None:
        """Test enum value comparison."""
        status = TaskStatus.INCOMPLETE
        assert status == TaskStatus.INCOMPLETE
        assert status != TaskStatus.COMPLETE


class TestTaskCreation:
    """Tests for Task entity creation."""

    def test_create_task_with_title_only(self) -> None:
        """Test creating task with title only."""
        task = Task(task_id=1, title="Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE

    def test_create_task_with_title_and_description(self) -> None:
        """Test creating task with title and description."""
        task = Task(task_id=1, title="Buy groceries", description="Milk, eggs, bread")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.status == TaskStatus.INCOMPLETE

    def test_create_task_with_custom_status(self) -> None:
        """Test creating task with custom status."""
        task = Task(
            task_id=1, title="Task", status=TaskStatus.COMPLETE
        )
        assert task.status == TaskStatus.COMPLETE

    def test_task_created_at_defaults_to_now(self) -> None:
        """Test that created_at defaults to current time."""
        before = datetime.now()
        task = Task(task_id=1, title="Task")
        after = datetime.now()
        assert before <= task.created_at <= after

    def test_task_created_at_can_be_set(self) -> None:
        """Test that created_at can be explicitly set."""
        custom_time = datetime(2025, 1, 1, 12, 0, 0)
        task = Task(task_id=1, title="Task", created_at=custom_time)
        assert task.created_at == custom_time

    def test_task_id_immutable(self) -> None:
        """Test that task ID cannot be changed after creation."""
        task = Task(task_id=1, title="Task")
        assert task.id == 1
        # Attempting to change should fail (attribute assignment)
        with pytest.raises(AttributeError):
            task.id = 2


class TestTaskMethods:
    """Tests for Task entity methods."""

    def test_update_title(self) -> None:
        """Test updating task title."""
        task = Task(task_id=1, title="Original")
        task.update_title("Updated")
        assert task.title == "Updated"

    def test_update_description(self) -> None:
        """Test updating task description."""
        task = Task(task_id=1, title="Task", description="Original")
        task.update_description("Updated")
        assert task.description == "Updated"

    def test_mark_complete(self) -> None:
        """Test marking task as complete."""
        task = Task(task_id=1, title="Task")
        assert task.status == TaskStatus.INCOMPLETE
        task.mark_complete()
        assert task.status == TaskStatus.COMPLETE

    def test_mark_incomplete(self) -> None:
        """Test marking task as incomplete."""
        task = Task(task_id=1, title="Task", status=TaskStatus.COMPLETE)
        assert task.status == TaskStatus.COMPLETE
        task.mark_incomplete()
        assert task.status == TaskStatus.INCOMPLETE

    def test_is_complete_true(self) -> None:
        """Test is_complete returns True for complete tasks."""
        task = Task(task_id=1, title="Task", status=TaskStatus.COMPLETE)
        assert task.is_complete() is True

    def test_is_complete_false(self) -> None:
        """Test is_complete returns False for incomplete tasks."""
        task = Task(task_id=1, title="Task")
        assert task.is_complete() is False

    def test_repr(self) -> None:
        """Test string representation of task."""
        task = Task(task_id=1, title="Buy groceries")
        assert "[1]" in repr(task)
        assert "○" in repr(task)  # Incomplete symbol
        assert "Buy groceries" in repr(task)

        task.mark_complete()
        assert "✓" in repr(task)  # Complete symbol


class TestTaskDataPersistence:
    """Tests for task data consistency."""

    def test_update_preserves_id(self) -> None:
        """Test that ID is never changed by update operations."""
        task = Task(task_id=1, title="Original")
        task.update_title("Updated")
        assert task.id == 1

    def test_status_change_preserves_title(self) -> None:
        """Test that status change doesn't affect title."""
        task = Task(task_id=1, title="Original")
        task.mark_complete()
        assert task.title == "Original"

    def test_status_change_preserves_description(self) -> None:
        """Test that status change doesn't affect description."""
        task = Task(task_id=1, title="Task", description="Desc")
        task.mark_complete()
        assert task.description == "Desc"
