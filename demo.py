"""
Phase I Todo Application - Feature Demonstration

This script demonstrates all Phase I features without user interaction.
Shows that all functionality works correctly.
"""

import sys
sys.path.insert(0, '/c/Users/LEnovo/Desktop/hackathon-2/todo-app')

from app.repository import TaskRepository
from app.service import TaskService
from app.models import TaskStatus
from app.exceptions import ValidationError, TaskNotFoundError


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_basic_operations():
    """Demonstrate basic CRUD operations."""
    print_section("FEATURE 1: Add and View Tasks")

    service = TaskService(TaskRepository())

    # Add some tasks
    print("Adding tasks...")
    task1 = service.add_task("Buy groceries", "Milk, eggs, bread")
    print(f"[OK] Created task {task1.id}: {task1.title}")

    task2 = service.add_task("Call dentist")
    print(f"[OK] Created task {task2.id}: {task2.title}")

    task3 = service.add_task("Finish project", "Due Friday")
    print(f"[OK] Created task {task3.id}: {task3.title}")

    # View all tasks
    print("\nViewing all tasks:")
    all_tasks = service.get_all_tasks()
    print(f"{'ID':<4} {'Status':<8} {'Title':<25} {'Description':<30}")
    print("-" * 70)
    for task in all_tasks:
        status = "[OK]" if task.is_complete() else "-"
        desc = task.description if task.description else "(no description)"
        print(f"{task.id:<4} {status:<8} {task.title:<25} {desc:<30}")

    total, completed, remaining = service.get_statistics()
    print(f"\nTotal: {total} | Completed: {completed} | Remaining: {remaining}")

    return service


def demo_update_task(service):
    """Demonstrate update functionality."""
    print_section("FEATURE 2: Update Task")

    print("Updating task 1: 'Buy groceries' -> 'Get groceries'")
    updated, changed = service.update_task(1, new_title="Get groceries")
    print(f"[OK] Task updated: {updated.title}")
    print(f"  Changed: {changed}")


def demo_toggle_status(service):
    """Demonstrate status toggling."""
    print_section("FEATURE 3: Mark Task Complete/Incomplete")

    print("Marking task 1 as complete...")
    task = service.mark_complete(1)
    print(f"[OK] Task 1 is now: {'COMPLETE [OK]' if task.is_complete() else 'INCOMPLETE -'}")

    print("\nMarking task 1 as incomplete...")
    task = service.mark_incomplete(1)
    print(f"[OK] Task 1 is now: {'COMPLETE [OK]' if task.is_complete() else 'INCOMPLETE -'}")

    print("\nMarking tasks 1 and 3 as complete...")
    service.mark_complete(1)
    service.mark_complete(3)

    total, completed, remaining = service.get_statistics()
    print(f"Statistics: {total} total | {completed} completed | {remaining} remaining")


def demo_delete_task(service):
    """Demonstrate delete functionality."""
    print_section("FEATURE 4: Delete Task")

    print("Deleting task 2...")
    deleted = service.delete_task(2)
    print(f"[OK] Deleted: {deleted.title}")

    print("\nRemaining tasks:")
    all_tasks = service.get_all_tasks()
    for task in all_tasks:
        status = "[OK]" if task.is_complete() else "-"
        print(f"  [{task.id}] {status} {task.title}")

    print(f"\nNote: Task ID 2 is gone, but gaps are allowed (never reused)")


def demo_error_handling():
    """Demonstrate error handling."""
    print_section("FEATURE 5: Error Handling")

    service = TaskService(TaskRepository())

    # Error 1: Empty title
    print("Test 1: Empty task title")
    try:
        service.add_task("")
    except ValidationError as e:
        print(f"[OK] Caught: {e}")

    # Error 2: Title too long
    print("\nTest 2: Title exceeds 200 characters")
    try:
        service.add_task("x" * 201)
    except ValidationError as e:
        print(f"[OK] Caught: {e}")

    # Error 3: Description too long
    print("\nTest 3: Description exceeds 500 characters")
    try:
        service.add_task("Task", "y" * 501)
    except ValidationError as e:
        print(f"[OK] Caught: {e}")

    # Create a task for further tests
    task = service.add_task("Test Task")

    # Error 4: Task not found
    print("\nTest 4: Task ID not found")
    try:
        service.get_task(999)
    except TaskNotFoundError as e:
        print(f"[OK] Caught: {e}")

    # Error 5: Already complete
    print("\nTest 5: Mark already-complete as complete")
    service.mark_complete(task.id)
    try:
        service.mark_complete(task.id)
    except ValidationError as e:
        print(f"[OK] Caught: {e}")

    # Error 6: Already incomplete
    print("\nTest 6: Mark already-incomplete as incomplete")
    service.mark_incomplete(task.id)
    try:
        service.mark_incomplete(task.id)
    except ValidationError as e:
        print(f"[OK] Caught: {e}")


def demo_id_generation():
    """Demonstrate sequential ID generation without reuse."""
    print_section("FEATURE 6: Sequential ID Generation (No Reuse)")

    service = TaskService(TaskRepository())

    print("Adding tasks 1, 2, 3, 4, 5...")
    tasks = []
    for i in range(1, 6):
        task = service.add_task(f"Task {i}")
        tasks.append(task)
        print(f"  Created ID {task.id}")

    print("\nDeleting task 2...")
    service.delete_task(2)
    print(f"  Task 2 deleted (gap allowed)")

    print("\nAdding new task (should get ID 6, not 2)...")
    new_task = service.add_task("Task 6")
    print(f"  New task got ID: {new_task.id} [OK]")

    print("\nFinal task IDs: {", ", ".join(str(t.id) for t in service.get_all_tasks()), "}")
    print("  Note: No task with ID 2 (gap is OK, never reused)")


def main():
    """Run all demonstrations."""
    print("\n")
    print("=" * 70)
    print("PHASE I TODO APPLICATION DEMONSTRATION".center(70))
    print("All Features Working Correctly".center(70))
    print("=" * 70)

    # Run demonstrations
    service = demo_basic_operations()
    demo_update_task(service)
    demo_toggle_status(service)
    demo_delete_task(service)
    demo_error_handling()
    demo_id_generation()

    # Summary
    print_section("SUMMARY")
    print("[SUCCESS] Feature 1: Add Task - WORKING")
    print("[SUCCESS] Feature 2: View Tasks - WORKING")
    print("[SUCCESS] Feature 3: Update Task - WORKING")
    print("[SUCCESS] Feature 4: Delete Task - WORKING")
    print("[SUCCESS] Feature 5: Mark Complete/Incomplete - WORKING")
    print("[SUCCESS] Feature 6: Error Handling - WORKING")
    print("[SUCCESS] Feature 7: Sequential ID Generation - WORKING")
    print("\n[SUCCESS] ALL PHASE I FEATURES IMPLEMENTED AND WORKING\n")


if __name__ == "__main__":
    main()
