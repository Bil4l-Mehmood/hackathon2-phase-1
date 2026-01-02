"""
Unit tests for TaskRepository in-memory storage.

Tests the repository layer independently from service and CLI.
"""

import pytest
from app.models import Task, TaskStatus
from app.repository import TaskRepository


class TestRepositoryInitialization:
    """Tests for repository initialization."""

    def test_new_repository_is_empty(self) -> None:
        """Test that new repository starts empty."""
        repo = TaskRepository()
        assert repo.get_all_tasks() == []

    def test_new_repository_next_id_is_one(self) -> None:
        """Test that next_id starts at 1."""
        repo = TaskRepository()
        assert repo.get_next_id() == 1


class TestTaskAddition:
    """Tests for adding tasks to repository."""

    def test_add_single_task(self) -> None:
        """Test adding a single task."""
        repo = TaskRepository()
        task = Task(task_id=1, title="Test")
        repo.add_task(task)

        assert repo.task_exists(1)
        assert repo.get_task(1) == task

    def test_add_multiple_tasks(self) -> None:
        """Test adding multiple tasks."""
        repo = TaskRepository()
        task1 = Task(task_id=1, title="Task 1")
        task2 = Task(task_id=2, title="Task 2")

        repo.add_task(task1)
        repo.add_task(task2)

        assert len(repo.get_all_tasks()) == 2
        assert repo.get_task(1) == task1
        assert repo.get_task(2) == task2

    def test_add_task_returns_task(self) -> None:
        """Test that add_task returns the added task."""
        repo = TaskRepository()
        task = Task(task_id=1, title="Test")
        returned = repo.add_task(task)

        assert returned == task

    def test_add_task_updates_next_id(self) -> None:
        """Test that adding a task updates next_id."""
        repo = TaskRepository()
        task = Task(task_id=1, title="Test")
        repo.add_task(task)

        assert repo.get_next_id() == 2


class TestTaskRetrieval:
    """Tests for retrieving tasks from repository."""

    def test_get_existing_task(self) -> None:
        """Test getting an existing task."""
        repo = TaskRepository()
        task = Task(task_id=1, title="Test")
        repo.add_task(task)

        retrieved = repo.get_task(1)
        assert retrieved == task

    def test_get_nonexistent_task_returns_none(self) -> None:
        """Test that getting non-existent task returns None."""
        repo = TaskRepository()
        assert repo.get_task(99) is None

    def test_get_all_tasks_empty(self) -> None:
        """Test get_all_tasks on empty repository."""
        repo = TaskRepository()
        assert repo.get_all_tasks() == []

    def test_get_all_tasks_sorted(self) -> None:
        """Test that get_all_tasks returns tasks sorted by ID."""
        repo = TaskRepository()
        task3 = Task(task_id=3, title="Task 3")
        task1 = Task(task_id=1, title="Task 1")
        task2 = Task(task_id=2, title="Task 2")

        # Add out of order
        repo.add_task(task3)
        repo.add_task(task1)
        repo.add_task(task2)

        all_tasks = repo.get_all_tasks()
        assert [t.id for t in all_tasks] == [1, 2, 3]


class TestTaskDeletion:
    """Tests for deleting tasks from repository."""

    def test_delete_existing_task(self) -> None:
        """Test deleting an existing task."""
        repo = TaskRepository()
        task = Task(task_id=1, title="Test")
        repo.add_task(task)

        assert repo.delete_task(1) is True
        assert not repo.task_exists(1)

    def test_delete_nonexistent_task(self) -> None:
        """Test deleting a non-existent task returns False."""
        repo = TaskRepository()
        assert repo.delete_task(99) is False

    def test_delete_removes_from_list(self) -> None:
        """Test that deleted task is removed from get_all_tasks."""
        repo = TaskRepository()
        task1 = Task(task_id=1, title="Task 1")
        task2 = Task(task_id=2, title="Task 2")

        repo.add_task(task1)
        repo.add_task(task2)

        repo.delete_task(1)

        all_tasks = repo.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == 2


class TestTaskExistence:
    """Tests for checking task existence."""

    def test_task_exists_true(self) -> None:
        """Test task_exists returns True for existing task."""
        repo = TaskRepository()
        task = Task(task_id=1, title="Test")
        repo.add_task(task)

        assert repo.task_exists(1) is True

    def test_task_exists_false(self) -> None:
        """Test task_exists returns False for non-existent task."""
        repo = TaskRepository()
        assert repo.task_exists(1) is False


class TestIDGeneration:
    """Tests for sequential ID generation strategy."""

    def test_id_generation_sequential(self) -> None:
        """Test that IDs increment sequentially."""
        repo = TaskRepository()

        id1 = repo.get_next_id()
        task1 = Task(task_id=id1, title="Task 1")
        repo.add_task(task1)

        id2 = repo.get_next_id()
        assert id2 == id1 + 1

        task2 = Task(task_id=id2, title="Task 2")
        repo.add_task(task2)

        id3 = repo.get_next_id()
        assert id3 == id2 + 1

    def test_id_never_reused_after_deletion(self) -> None:
        """Test that IDs are never reused, even after deletion."""
        repo = TaskRepository()

        # Create tasks 1, 2, 3
        task1 = Task(task_id=1, title="Task 1")
        task2 = Task(task_id=2, title="Task 2")
        task3 = Task(task_id=3, title="Task 3")

        repo.add_task(task1)
        repo.add_task(task2)
        repo.add_task(task3)

        # Delete task 2
        repo.delete_task(2)

        # Next ID should be 4, not 2
        id_after_delete = repo.get_next_id()
        assert id_after_delete == 4

        task4 = Task(task_id=id_after_delete, title="Task 4")
        repo.add_task(task4)

        # Check final state: tasks 1, 3, 4 exist; 2 does not
        assert repo.task_exists(1)
        assert not repo.task_exists(2)
        assert repo.task_exists(3)
        assert repo.task_exists(4)


class TestRepositoryClear:
    """Tests for clearing repository."""

    def test_clear_removes_all_tasks(self) -> None:
        """Test that clear removes all tasks."""
        repo = TaskRepository()
        task1 = Task(task_id=1, title="Task 1")
        task2 = Task(task_id=2, title="Task 2")

        repo.add_task(task1)
        repo.add_task(task2)

        repo.clear()

        assert repo.get_all_tasks() == []

    def test_clear_resets_next_id(self) -> None:
        """Test that clear resets next_id to 1."""
        repo = TaskRepository()
        task = Task(task_id=1, title="Task")
        repo.add_task(task)

        repo.clear()

        assert repo.get_next_id() == 1
