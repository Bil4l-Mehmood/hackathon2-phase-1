"""
Integration tests for complete workflows.

Tests full workflows across multiple features to verify system integration.
"""

from app.models import TaskStatus
from app.repository import TaskRepository
from app.service import TaskService


class TestCompleteWorkflows:
    """Integration tests for complete todo application workflows."""

    def test_add_and_view_workflow(self) -> None:
        """Test adding tasks and viewing them."""
        service = TaskService(TaskRepository())

        # Add tasks
        task1 = service.add_task("Buy groceries")
        task2 = service.add_task("Call dentist", "Appointment")
        task3 = service.add_task("Finish project")

        # View all tasks
        all_tasks = service.get_all_tasks()

        assert len(all_tasks) == 3
        assert all_tasks[0].title == "Buy groceries"
        assert all_tasks[1].title == "Call dentist"
        assert all_tasks[2].title == "Finish project"

    def test_add_update_view_workflow(self) -> None:
        """Test adding, updating, and viewing tasks."""
        service = TaskService(TaskRepository())

        # Add task
        task = service.add_task("Buy groceries")

        # Update task
        updated, _ = service.update_task(
            task.id, new_title="Get groceries", new_description="Milk, eggs, bread"
        )

        # View and verify
        viewed = service.get_task(task.id)

        assert viewed.title == "Get groceries"
        assert viewed.description == "Milk, eggs, bread"
        assert viewed.status == TaskStatus.INCOMPLETE

    def test_add_delete_view_workflow(self) -> None:
        """Test adding, deleting, and viewing tasks."""
        service = TaskService(TaskRepository())

        # Add tasks
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        # Delete task 2
        deleted = service.delete_task(task2.id)

        # View remaining
        all_tasks = service.get_all_tasks()

        assert deleted.id == 2
        assert len(all_tasks) == 2
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 3

    def test_add_mark_complete_view_workflow(self) -> None:
        """Test adding, marking complete, and viewing."""
        service = TaskService(TaskRepository())

        # Add tasks
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        # Mark some as complete
        service.mark_complete(task1.id)
        service.mark_complete(task3.id)

        # View and verify
        all_tasks = service.get_all_tasks()

        assert all_tasks[0].is_complete()
        assert not all_tasks[1].is_complete()
        assert all_tasks[2].is_complete()

        # Verify statistics
        total, completed, remaining = service.get_statistics()
        assert total == 3
        assert completed == 2
        assert remaining == 1

    def test_complex_workflow(self) -> None:
        """Test complex workflow with multiple operations."""
        service = TaskService(TaskRepository())

        # Add multiple tasks
        t1 = service.add_task("Buy groceries", "Milk, eggs, bread")
        t2 = service.add_task("Call dentist")
        t3 = service.add_task("Finish project")
        t4 = service.add_task("Learn Python")

        # Initial statistics
        total, completed, remaining = service.get_statistics()
        assert total == 4
        assert completed == 0
        assert remaining == 4

        # Mark some complete
        service.mark_complete(t1.id)
        service.mark_complete(t3.id)

        # Update a task
        service.update_task(t2.id, new_description="Next week")

        # Delete a task
        service.delete_task(t4.id)

        # Final verification
        final_tasks = service.get_all_tasks()
        assert len(final_tasks) == 3

        # Verify IDs are preserved (4 is deleted, gap allowed)
        ids = [t.id for t in final_tasks]
        assert ids == [1, 2, 3]
        assert 4 not in ids

        # Verify final statistics
        total, completed, remaining = service.get_statistics()
        assert total == 3
        assert completed == 2  # Tasks 1 and 3
        assert remaining == 1  # Task 2

        # Verify task details
        task2 = service.get_task(2)
        assert task2.title == "Call dentist"
        assert task2.description == "Next week"
        assert not task2.is_complete()

    def test_multiple_updates_workflow(self) -> None:
        """Test task with multiple sequential updates."""
        service = TaskService(TaskRepository())

        # Add task
        task = service.add_task("Original", "Desc 1")

        # Update title
        updated, changed = service.update_task(task.id, new_title="Updated Title")
        assert changed is True
        assert updated.title == "Updated Title"
        assert updated.description == "Desc 1"

        # Update description
        updated, changed = service.update_task(task.id, new_description="Desc 2")
        assert changed is True
        assert updated.title == "Updated Title"
        assert updated.description == "Desc 2"

        # Update both
        updated, changed = service.update_task(
            task.id, new_title="Final", new_description="Final Desc"
        )
        assert changed is True
        assert updated.title == "Final"
        assert updated.description == "Final Desc"

        # Verify persisted
        verified = service.get_task(task.id)
        assert verified.title == "Final"
        assert verified.description == "Final Desc"

    def test_toggle_status_multiple_times(self) -> None:
        """Test toggling task status back and forth."""
        service = TaskService(TaskRepository())

        task = service.add_task("Test")

        # Initially incomplete
        assert not task.is_complete()

        # Mark complete
        task = service.mark_complete(task.id)
        assert task.is_complete()

        # Mark incomplete
        task = service.mark_incomplete(task.id)
        assert not task.is_complete()

        # Mark complete again
        task = service.mark_complete(task.id)
        assert task.is_complete()

        # Verify in list
        viewed = service.get_task(task.id)
        assert viewed.is_complete()

    def test_id_never_reused_after_delete(self) -> None:
        """Test that task IDs are never reused after deletion."""
        service = TaskService(TaskRepository())

        # Create tasks 1, 2, 3
        t1 = service.add_task("Task 1")
        t2 = service.add_task("Task 2")
        t3 = service.add_task("Task 3")

        assert t1.id == 1
        assert t2.id == 2
        assert t3.id == 3

        # Delete task 2
        service.delete_task(2)

        # Create new task - should get ID 4, not 2
        t4 = service.add_task("Task 4")
        assert t4.id == 4

        # Create another
        t5 = service.add_task("Task 5")
        assert t5.id == 5

        # Verify final state
        all_tasks = service.get_all_tasks()
        ids = [t.id for t in all_tasks]
        assert ids == [1, 3, 4, 5]  # 2 is gap
        assert 2 not in ids

    def test_empty_list_stays_empty_after_add_delete(self) -> None:
        """Test that deleting all tasks returns to empty state."""
        service = TaskService(TaskRepository())

        # Empty start
        assert len(service.get_all_tasks()) == 0

        # Add and delete
        t1 = service.add_task("Task 1")
        t2 = service.add_task("Task 2")
        assert len(service.get_all_tasks()) == 2

        service.delete_task(t1.id)
        service.delete_task(t2.id)
        assert len(service.get_all_tasks()) == 0

        # Add new task after emptying
        t3 = service.add_task("Task 3")
        assert len(service.get_all_tasks()) == 1
        assert service.get_all_tasks()[0].id == 3

    def test_large_number_of_tasks(self) -> None:
        """Test with larger number of tasks (stress test)."""
        service = TaskService(TaskRepository())

        # Add 100 tasks
        for i in range(1, 101):
            service.add_task(f"Task {i}")

        # Verify
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 100
        assert all_tasks[0].id == 1
        assert all_tasks[99].id == 100

        # Statistics
        total, completed, remaining = service.get_statistics()
        assert total == 100
        assert completed == 0
        assert remaining == 100

        # Mark some complete
        for task in all_tasks[:50]:
            service.mark_complete(task.id)

        # Verify
        total, completed, remaining = service.get_statistics()
        assert total == 100
        assert completed == 50
        assert remaining == 50
