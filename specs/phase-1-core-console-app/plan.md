# Phase I: Core Console Todo Application - Architecture Plan

**Version**: 1.0.0 | **Date**: 2025-12-30 | **Phase**: I (Foundation)

**Constitutional Alignment**: ✅ Complies with EVOLUTION_CONSTITUTION.md Part V (Clean Architecture), Part VI (Development Workflow)

**Specification Reference**: `phase-1-core-console-app/spec.md`

---

## 1. Executive Summary

This plan describes HOW Phase I requirements will be implemented in a single Python console application. The architecture follows clean architecture principles with strict separation between domain logic (Task handling) and interface logic (CLI). All design decisions are driven by the Phase I specification and will not introduce Phase II+ concepts.

**Key Architecture Decisions**:
1. Domain layer isolation: Task entity and business logic independent of CLI
2. Service layer: Task operations (add, view, update, delete, toggle) as testable functions
3. CLI layer: Menu-driven interface separate from domain logic
4. In-memory storage: Python dict for task storage (no persistence, no databases)
5. Sequential ID generation: Max-based strategy for simple, predictable IDs
6. Error handling: Typed exceptions at domain layer, user-friendly messages at CLI layer

---

## 2. High-Level Application Structure

### 2.1 Application Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    MAIN APPLICATION                      │
│                   (main.py, __init__.py)                │
└─────────────────────────────────────────────────────────┘
                             │
                             ├─────────────────────────────┬──────────────────────┐
                             │                             │                      │
                             ▼                             ▼                      ▼
                      ┌──────────────┐          ┌──────────────────┐    ┌──────────────────┐
                      │  CLI LAYER   │          │ SERVICE LAYER    │    │  DOMAIN LAYER    │
                      │ (ui.py)      │          │ (service.py)     │    │ (models.py)      │
                      └──────────────┘          └──────────────────┘    └──────────────────┘
                             │                         │                         │
                             │                         │                         │
        ┌────────────────────┴─────────────────────────┴─────────────────────────┴──────────┐
        │                                                                                    │
        │   ┌─────────────────────────────────────────────────────────────────────────┐   │
        │   │            IN-MEMORY DATA STORE (TaskRepository)                       │   │
        │   │  tasks: Dict[int, Task]                                               │   │
        │   └─────────────────────────────────────────────────────────────────────────┘   │
        │                                                                                    │
        │   ┌─────────────────────────────────────────────────────────────────────────┐   │
        │   │              EXCEPTION HANDLING (exceptions.py)                        │   │
        │   │  TaskNotFoundError, ValidationError, etc.                             │   │
        │   └─────────────────────────────────────────────────────────────────────────┘   │
        │                                                                                    │
        └────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Module Organization

```
app/
├── main.py                 # Entry point, application initialization
├── __init__.py            # Package initialization
├── models.py              # Domain layer: Task entity
├── service.py             # Service layer: Task operations
├── ui.py                  # CLI layer: Menu and user interaction
├── exceptions.py          # Custom exceptions
└── repository.py          # In-memory storage management

tests/
├── __init__.py
├── test_models.py         # Task model tests
├── test_service.py        # Task service tests
├── test_ui.py            # CLI interaction tests
└── test_integration.py    # End-to-end workflow tests

requirements.txt           # Python dependencies (minimal)
README.md                  # Project documentation
```

### 2.3 Execution Flow

```
START (main.py)
  │
  ├─→ Initialize TaskRepository (empty)
  │
  └─→ Start REPL Loop
       │
       ├─→ Display Main Menu
       │
       ├─→ Accept User Input
       │
       ├─→ Validate Menu Selection (1-6)
       │   ├─ Invalid? Show error, loop back
       │   └─ Valid? Continue
       │
       ├─→ Execute Selected Action
       │   ├─ [1] Call add_task_flow()
       │   ├─ [2] Call view_tasks_flow()
       │   ├─ [3] Call update_task_flow()
       │   ├─ [4] Call delete_task_flow()
       │   ├─ [5] Call toggle_task_flow()
       │   └─ [6] EXIT
       │
       ├─→ Handle Errors
       │   ├─ ValidationError → Show user message, loop back
       │   ├─ TaskNotFoundError → Show user message, loop back
       │   └─ Other exceptions → Handle gracefully
       │
       └─→ Return to Menu Loop (until EXIT or EOF)
         │
         └─→ END
```

---

## 3. Domain Layer: Task Entity

### 3.1 Task Model Class

```python
# models.py

from enum import Enum
from datetime import datetime
from typing import Optional

class TaskStatus(Enum):
    """Task completion status."""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

class Task:
    """
    Task domain entity.

    Represents a single todo task with immutable ID and mutable
    title, description, and status.

    Attributes:
        id: Unique sequential task ID (immutable)
        title: Task title, 1-200 chars (mutable)
        description: Optional task description, max 500 chars (mutable)
        status: Task completion status (mutable)
        created_at: Task creation timestamp (immutable)
    """

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        status: TaskStatus = TaskStatus.INCOMPLETE,
        created_at: Optional[datetime] = None
    ):
        """
        Initialize a Task.

        Args:
            task_id: Unique sequential ID
            title: Task title (required)
            description: Task description (optional)
            status: Task status (defaults to INCOMPLETE)
            created_at: Creation timestamp (defaults to now)
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now()

    def update_title(self, new_title: str) -> None:
        """Update task title."""
        self.title = new_title

    def update_description(self, new_description: str) -> None:
        """Update task description."""
        self.description = new_description

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.status = TaskStatus.COMPLETE

    def mark_incomplete(self) -> None:
        """Mark task as incomplete."""
        self.status = TaskStatus.INCOMPLETE

    def is_complete(self) -> bool:
        """Check if task is complete."""
        return self.status == TaskStatus.COMPLETE

    def __repr__(self) -> str:
        """String representation of task."""
        status_symbol = "✓" if self.is_complete() else "○"
        return f"[{self.id}] {status_symbol} {self.title}"
```

### 3.2 Task Constraints (Validation at Domain Level)

**Title Constraints**:
- Required: Must be present
- Length: 1-200 characters
- Whitespace: Trimmed, no leading/trailing spaces, no empty after trim

**Description Constraints**:
- Optional: May be empty
- Length: 0-500 characters

**Status Constraints**:
- Enum: Only COMPLETE or INCOMPLETE
- Default: INCOMPLETE

**ID Constraints**:
- Unique: Never duplicated
- Sequential: Start at 1, increment by 1
- Immutable: Never changes after creation
- No reuse: Gaps allowed after deletion, next ID = max + 1

---

## 4. In-Memory Data Structures

### 4.1 TaskRepository (In-Memory Storage)

```python
# repository.py

from typing import Dict, List, Optional
from models import Task

class TaskRepository:
    """
    In-memory task repository.

    Manages task storage in a Python dictionary.
    Handles task persistence in memory and ID generation.
    """

    def __init__(self):
        """Initialize empty task storage."""
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
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks, sorted by ID."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def task_exists(self, task_id: int) -> bool:
        """Check if task exists."""
        return task_id in self._tasks

    def get_next_id(self) -> int:
        """Get the next available task ID."""
        return self._next_id

    def clear(self) -> None:
        """Clear all tasks (for testing)."""
        self._tasks.clear()
        self._next_id = 1
```

### 4.2 Data Structure Design Rationale

**Why Python Dict?**
- O(1) lookup by ID
- Simple and built-in (no external dependencies)
- In-memory storage (no persistence needed)
- Efficient for Phase I's expected task count (<1000)

**Why Sequential IDs?**
- Predictable: Easy to understand for users
- Simple: Max-based generation (no UUID complexity)
- Human-readable: Users can remember task IDs
- Specification requirement: "IDs start at 1, increment sequentially"

**Why Separate Repository?**
- Testability: Task service tests don't depend on CLI
- Encapsulation: Storage implementation can change later (Phase II may add persistence)
- Clean architecture: Data access logic isolated

---

## 5. Task Identification Strategy

### 5.1 ID Generation Algorithm

```
Algorithm: Sequential ID Generation

Current State:
  next_id = 1
  tasks = {}

When Adding Task:
  task.id = next_id
  tasks[task.id] = task
  next_id = next_id + 1
  return task.id

When Deleting Task:
  delete tasks[task_id]
  // Do NOT decrement next_id (ID gaps are allowed)
  // This ensures IDs are never reused

When Starting Application:
  next_id = 1
  tasks = {} (empty)
```

### 5.2 Implementation Example

```python
# In repository.py

class TaskRepository:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create_task_id(self) -> int:
        """Generate next task ID."""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add_task(self, title: str, description: str = "") -> Task:
        """Create and add task with auto-generated ID."""
        task_id = self.create_task_id()
        task = Task(task_id, title, description)
        self._tasks[task_id] = task
        return task
```

### 5.3 ID Lifecycle Example

```
Operations:        Task Storage:      next_id:
┌──────────────────────────────────────────────┐
│ Create Task 1    │ {1: Task}        │ 2      │
├──────────────────────────────────────────────┤
│ Create Task 2    │ {1: Task, 2: Task}    │ 3      │
├──────────────────────────────────────────────┤
│ Create Task 3    │ {1, 2, 3: Task}   │ 4      │
├──────────────────────────────────────────────┤
│ Delete Task 2    │ {1: Task, 3: Task}    │ 4      │ (gap allowed)
├──────────────────────────────────────────────┤
│ Create Task 4    │ {1, 3, 4: Task}   │ 5      │ (next_id continues)
└──────────────────────────────────────────────┘
```

---

## 6. Service Layer: Task Operations

### 6.1 TaskService Class

```python
# service.py

from typing import List, Tuple
from models import Task, TaskStatus
from repository import TaskRepository
from exceptions import TaskNotFoundError, ValidationError

class TaskService:
    """
    Task service layer.

    Coordinates task operations between domain and CLI layers.
    Performs business logic and validation.
    Does not interact with CLI directly.
    """

    def __init__(self, repository: TaskRepository):
        """Initialize service with repository."""
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
            ValidationError: If title is invalid
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
            Validated description

        Raises:
            ValidationError: If description is invalid
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
            title: Task title
            description: Task description (optional)

        Returns:
            Created Task

        Raises:
            ValidationError: If title/description invalid
        """
        validated_title = self.validate_title(title)
        validated_description = self.validate_description(description)

        task = Task(
            task_id=self.repo.get_next_id(),
            title=validated_title,
            description=validated_description
        )

        return self.repo.add_task(task)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks sorted by ID."""
        return self.repo.get_all_tasks()

    def get_task(self, task_id: int) -> Task:
        """
        Get a task by ID.

        Args:
            task_id: Task ID

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
        new_title: str = None,
        new_description: str = None
    ) -> Tuple[Task, bool]:
        """
        Update a task's title and/or description.

        Args:
            task_id: Task ID to update
            new_title: New title (None = no change)
            new_description: New description (None = no change)

        Returns:
            Tuple of (updated Task, was_changed)

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
            task_id: Task ID

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
            task_id: Task ID

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
```

### 6.2 Service Layer Design Rationale

**Why Service Layer?**
- Testability: Business logic tested independently of CLI
- Reusability: Can be used by different interfaces (CLI, API, GUI)
- Maintainability: Business logic in one place
- Separation of Concerns: Service doesn't know about user interaction

**Validation Strategy**:
- Validation happens at service entry points
- Domain model assumes valid data (no redundant validation)
- Clear, user-friendly error messages at service level
- Validation errors are caught and displayed by CLI

**Exception Design**:
- Custom exceptions for different error types
- Exceptions carry error messages for CLI display
- No exception handling in service layer (let CLI decide)

---

## 7. CLI Control Flow

### 7.1 CLI Architecture

```python
# ui.py

from models import TaskStatus
from service import TaskService
from repository import TaskRepository
from exceptions import ValidationError, TaskNotFoundError

class TodoApp:
    """
    Command-line interface for Todo application.

    Handles user interaction and menu-driven flow.
    Translates user input to service calls.
    Displays results and error messages.
    """

    def __init__(self):
        """Initialize CLI with repository and service."""
        self.repo = TaskRepository()
        self.service = TaskService(self.repo)

    def run(self) -> None:
        """Start the application."""
        print("========== TODO APPLICATION ==========")
        print("Type 'help' for commands or 'exit' to quit\n")

        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 6:  # Exit
                print("Goodbye!")
                break

            try:
                self.execute_action(choice)
            except (ValidationError, TaskNotFoundError) as e:
                print(f"Error: {str(e)}")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")

            print()  # Blank line for readability

    # --- Menu Management ---

    def show_menu(self) -> None:
        """Display main menu."""
        print("========== TODO APPLICATION ==========")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print()

    def get_menu_choice(self) -> int:
        """Get and validate menu selection from user."""
        while True:
            try:
                choice_str = input("Choose an option (1-6): ").strip()
                choice = int(choice_str)

                if 1 <= choice <= 6:
                    return choice
                else:
                    print("Error: Please enter a number between 1 and 6")
            except ValueError:
                print("Error: Please enter a number between 1 and 6")

    def execute_action(self, choice: int) -> None:
        """Execute selected action."""
        actions = {
            1: self.action_add_task,
            2: self.action_view_tasks,
            3: self.action_update_task,
            4: self.action_delete_task,
            5: self.action_toggle_status,
        }

        action = actions.get(choice)
        if action:
            action()

    # --- User Input Helpers ---

    def get_text_input(
        self,
        prompt: str,
        required: bool = False,
        max_length: int = None
    ) -> str:
        """Get user text input with optional validation."""
        while True:
            value = input(prompt)

            if not required and value == "":
                return ""

            if required and not value.strip():
                print("Error: Input cannot be empty")
                continue

            if max_length and len(value) > max_length:
                print(f"Error: Input exceeds {max_length} characters")
                continue

            return value

    def get_numeric_input(self, prompt: str) -> int:
        """Get numeric input from user."""
        while True:
            try:
                value = input(prompt).strip()
                return int(value)
            except ValueError:
                print("Error: Task ID must be a number")

    def get_confirmation(self) -> bool:
        """Get y/n confirmation from user."""
        while True:
            response = input("Confirm? (y/n): ").strip().lower()
            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print("Error: Please enter 'y' or 'n'")

    # --- Action Methods ---

    def action_add_task(self) -> None:
        """Action: Add a new task."""
        print("\n--- Add Task ---")
        title = self.get_text_input("Enter task title: ", required=True)
        description = self.get_text_input(
            "Enter task description (press Enter to skip): ",
            required=False
        )

        task = self.service.add_task(title, description)

        print(f"✓ Task created with ID: {task.id}")
        print(f"Task: \"{task.title}\" [{task.status.value}]")

    def action_view_tasks(self) -> None:
        """Action: View all tasks."""
        print("\n--- Your Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks yet")
            return

        print(f"{'ID':<4} {'Status':<8} {'Title':<25} {'Description':<30}")
        print("-" * 70)

        for task in tasks:
            status_symbol = "✓" if task.is_complete() else "○"
            desc_display = task.description or "(no description)"
            print(
                f"{task.id:<4} {status_symbol:<8} "
                f"{task.title:<25} {desc_display:<30}"
            )

        print("-" * 70)
        total, completed, remaining = self.service.get_statistics()
        print(
            f"Total: {total} tasks | "
            f"Completed: {completed} | "
            f"Remaining: {remaining}"
        )

    def action_update_task(self) -> None:
        """Action: Update a task."""
        print("\n--- Update Task ---")
        task_id = self.get_numeric_input("Enter task ID to update: ")

        task = self.service.get_task(task_id)
        print(f"Current task: \"{task.title}\"", end="")
        if task.description:
            print(f" ({task.description})")
        else:
            print(" (no description)")

        print()
        new_title = self.get_text_input(
            "Enter new title (press Enter to keep current): ",
            required=False
        )
        new_description = self.get_text_input(
            "Enter new description (press Enter to keep current): ",
            required=False
        )

        # Use None to indicate "no change"
        updated_task, was_changed = self.service.update_task(
            task_id,
            new_title if new_title else None,
            new_description if new_description != "" else None
        )

        if not was_changed:
            print("No changes made. Task remains unchanged")
        else:
            print(f"✓ Task {task_id} updated successfully")
            print(f"Updated task: \"{updated_task.title}\"", end="")
            if updated_task.description:
                print(f" ({updated_task.description})")
            else:
                print(" (no description)")

    def action_delete_task(self) -> None:
        """Action: Delete a task."""
        print("\n--- Delete Task ---")
        task_id = self.get_numeric_input("Enter task ID to delete: ")

        task = self.service.get_task(task_id)
        print(f"Delete task? \"{task.title}\"", end="")
        if task.description:
            print(f" ({task.description})", end="")
        print()

        if self.get_confirmation():
            deleted_task = self.service.delete_task(task_id)
            print(f"✓ Task {task_id} deleted successfully")
        else:
            print("Deletion cancelled. Task remains")

    def action_toggle_status(self) -> None:
        """Action: Mark task complete/incomplete."""
        print("\n--- Mark Task Complete/Incomplete ---")
        task_id = self.get_numeric_input("Enter task ID: ")

        task = self.service.get_task(task_id)
        current_status = "✓ complete" if task.is_complete() else "○ incomplete"
        print(f"Current status: {current_status}")

        print()
        print("1. Mark Complete")
        print("2. Mark Incomplete")
        print()

        while True:
            try:
                choice = int(input("Choose (1-2): ").strip())
                if choice == 1:
                    updated_task = self.service.mark_complete(task_id)
                    print(f"✓ Task {task_id} marked as complete")
                    print(f"New status: ✓ complete")
                    break
                elif choice == 2:
                    updated_task = self.service.mark_incomplete(task_id)
                    print(f"✓ Task {task_id} marked as incomplete")
                    print(f"New status: ○ incomplete")
                    break
                else:
                    print("Error: Please enter 1 or 2")
            except ValueError:
                print("Error: Please enter 1 or 2")

# main.py

if __name__ == "__main__":
    app = TodoApp()
    app.run()
```

### 7.2 Menu Loop Design

```
MENU LOOP (main.py):

while True:
    1. Display Menu (6 options)
    2. Get User Input (validate 1-6)
    3. Invalid input?
       → Show error
       → Loop back to step 1
    4. Valid input?
       → Route to action handler
    5. Action Handler (validate task ID, call service, display result)
       → ValidationError caught?
         → Show error
         → Loop back to step 1
       → Success?
         → Show confirmation
         → Loop back to step 1
    6. Exit selected?
       → Break loop
       → End application
```

### 7.3 Error Handling at CLI Layer

```python
# Error handling strategy

try:
    # Execute service operation
    task = self.service.add_task(title, description)
except ValidationError as e:
    # Service validation error (title too long, etc.)
    print(f"Error: {str(e)}")
    return  # Return to menu
except TaskNotFoundError as e:
    # Task ID doesn't exist
    print(f"Error: {str(e)}")
    return  # Return to menu
except Exception as e:
    # Unexpected error (shouldn't happen in Phase I)
    print(f"Unexpected error: {str(e)}")
    return  # Return to menu
```

---

## 8. Error Handling Strategy

### 8.1 Exception Hierarchy

```python
# exceptions.py

class TodoAppException(Exception):
    """Base exception for Todo application."""
    pass

class ValidationError(TodoAppException):
    """Raised when user input validation fails."""
    pass

class TaskNotFoundError(TodoAppException):
    """Raised when task ID doesn't exist."""
    pass

class InvalidStatusError(TodoAppException):
    """Raised when invalid status transition attempted."""
    pass
```

### 8.2 Error Handling Flow

```
USER INPUT
    ↓
VALIDATE (CLI Layer)
    ├─ Invalid format? (non-numeric ID, etc.)
    │  ├─ Show error message
    │  └─ Retry input
    │
    └─ Valid format?
        ↓
    CALL SERVICE
        ↓
    SERVICE VALIDATION
        ├─ Validation error? (title too long, etc.)
        │  └─ Raise ValidationError
        │
        ├─ Logic error? (task not found, etc.)
        │  └─ Raise TaskNotFoundError
        │
        └─ Success?
            └─ Return result

        ↓
    CATCH EXCEPTION (CLI Layer)
        ├─ ValidationError
        │  ├─ Extract message
        │  ├─ Display to user
        │  └─ Return to menu
        │
        ├─ TaskNotFoundError
        │  ├─ Extract message
        │  ├─ Display to user
        │  └─ Return to menu
        │
        └─ Other exceptions
            ├─ Display unexpected error
            └─ Return to menu
```

### 8.3 Error Message Examples

| Scenario | Layer | Exception | Message |
|----------|-------|-----------|---------|
| User enters "abc" for menu | CLI | ValueError | "Error: Please enter a number between 1 and 6" |
| User enters "99" for menu | CLI | ValueError | "Error: Please enter a number between 1 and 6" |
| User enters empty title | Service | ValidationError | "Error: Task title cannot be empty" |
| User enters 300-char title | Service | ValidationError | "Error: Task title exceeds 200 characters" |
| User enters non-numeric task ID | CLI | ValueError | "Error: Task ID must be a number" |
| User enters non-existent task ID | Service | TaskNotFoundError | "Error: Task ID 99 not found" |
| User tries to mark complete→complete | Service | ValidationError | "Error: Task is already complete" |

---

## 9. Separation of Responsibilities

### 9.1 Layer Responsibilities

| Layer | Responsibility | Knows About | Does NOT Know About |
|-------|-----------------|-------------|---------------------|
| **Domain** | Task entity, constraints | Task fields, status, creation | User input, UI, storage format |
| **Repository** | In-memory storage | Dict of tasks, ID generation | User input, domain logic details |
| **Service** | Business logic, validation | Tasks, validation rules | User input, UI formatting |
| **CLI** | User interaction | Menu options, input prompts | Task internals, storage details |

### 9.2 Dependency Flow

```
CLI (ui.py)
  ↓ uses
Service (service.py)
  ↓ uses
Repository (repository.py)
  ↓ manages
Domain Models (models.py)

Reverse Direction (returns):
Domain Models
  ↓ returns to
Repository
  ↓ returns to
Service
  ↓ returns to
CLI
```

**Key Principle**: Each layer depends only on the layer below it, never upward.

### 9.3 Testing Implications

```
Domain Tests (test_models.py)
  - Test Task creation
  - Test Task methods
  - Depend only on models.py

Repository Tests (test_repository.py)
  - Test storage operations
  - Test ID generation
  - Depend on models.py and repository.py

Service Tests (test_service.py)
  - Test business logic
  - Test validation
  - Depend on models.py, repository.py, service.py
  - Mock repository for isolated testing

CLI Tests (test_ui.py)
  - Test input handling
  - Test menu navigation
  - Depend on ui.py, service.py, repository.py
  - Mock service for isolated UI testing

Integration Tests (test_integration.py)
  - Test complete workflows
  - Test all layers together
  - No mocking
```

---

## 10. Design Patterns Used

### 10.1 Repository Pattern
- **Purpose**: Abstract data storage from business logic
- **Implementation**: TaskRepository class
- **Benefit**: Easy to add persistence later (Phase II)

### 10.2 Service Pattern
- **Purpose**: Encapsulate business logic
- **Implementation**: TaskService class
- **Benefit**: Reusable across different UIs

### 10.3 Separation of Concerns
- **Purpose**: Domain, storage, business logic, and UI are independent
- **Implementation**: Four separate modules (models, repository, service, ui)
- **Benefit**: Changes in one layer don't require changes in others

### 10.4 Enum for Status
- **Purpose**: Type-safe status representation
- **Implementation**: TaskStatus enum
- **Benefit**: No stringly-typed status values

---

## 11. Constraints & Assumptions

### 11.1 Architectural Constraints

1. **Single Process**: Application runs as single Python process
2. **In-Memory Storage**: No persistence, all data lost on exit
3. **Single User**: No concurrent access or multi-user support
4. **No External Dependencies**: Standard library only (except test framework)
5. **Console Only**: Text input/output, no GUI
6. **Linear Scaling**: Designed for <1000 tasks

### 11.2 Design Assumptions

1. Task ID cannot be negative or zero
2. Task title is never None (always string, possibly empty)
3. Service validation is always performed before storage
4. CLI always catches exceptions and displays messages
5. User input is always through stdin (no programmatic input)

---

## 12. Migration Path to Phase II

This architecture is designed to support Phase II (REST API) with minimal changes:

### 12.1 Phase II Additions (Not in Phase I)

**What will be added**:
- HTTP endpoint layer (FastAPI)
- Persistence layer (PostgreSQL)
- Authentication middleware
- API request/response handling

**What won't change**:
- Domain models (Task, TaskStatus)
- Service layer (business logic)
- Repository interface (but implementation will change)
- Error handling strategy

### 12.2 Phase II Architecture

```
Client (HTTP)
    ↓
API Routes (FastAPI)  [NEW]
    ↓
Service (business logic)  [SAME]
    ↓
Repository (persistence)  [CHANGED IMPLEMENTATION]
    ↓
Database (PostgreSQL)  [NEW]

Domain Models  [SAME]
Exception Handling  [SAME]
```

The Service and Domain layers remain unchanged, making Phase II integration straightforward.

---

## 13. Testing Architecture

### 13.1 Test Organization

```
tests/
├── test_models.py           # Domain model tests
├── test_repository.py       # Storage tests
├── test_service.py          # Business logic tests
├── test_ui.py              # UI interaction tests
├── test_integration.py     # End-to-end workflows
├── conftest.py             # Pytest fixtures
└── __init__.py
```

### 13.2 Test Coverage Target

- **Domain** (models.py): 100% (critical, small code)
- **Repository** (repository.py): 100% (critical, small code)
- **Service** (service.py): 100% (critical business logic)
- **UI** (ui.py): 80%+ (user interaction, harder to test)
- **Overall**: 80% minimum

### 13.3 Testable Components

**Fully Testable** (without UI):
- Task model creation and methods
- ID generation algorithm
- Validation logic (title, description, task ID)
- CRUD operations
- Status transitions

**Requires Mocking**:
- User input (mock input())
- Console output (capture stdout)
- Interactive flows (simulate menu choices)

---

## 14. Out of Scope (NOT This Plan)

The following are **explicitly not** described in this plan:

- ❌ File persistence
- ❌ Database schema
- ❌ Authentication system
- ❌ REST API endpoints
- ❌ WebSocket connections
- ❌ Task categories or tags
- ❌ Due dates or priorities
- ❌ Task search or filtering
- ❌ Recurring tasks
- ❌ Task assignment or sharing
- ❌ Performance optimization (caching, indexing, etc.)
- ❌ Distributed systems
- ❌ Cloud deployment

---

## 15. Success Criteria

This plan is successful when:

✅ **Architecture is clear**: All layers and responsibilities are defined
✅ **Testable design**: Each layer can be tested independently
✅ **No feature bloat**: Plan describes Phase I only
✅ **Follows specification**: Every spec requirement has an architectural home
✅ **Follows constitution**: Clean architecture, separation of concerns applied
✅ **Phase II ready**: Design allows easy Phase II integration
✅ **Implementation ready**: Developers have clear blueprint

---

## 16. Compliance Checklist

- ✅ No Phase II+ features (API, persistence, auth, etc.)
- ✅ Follows Constitution Part V (Clean Architecture)
- ✅ Derives from specification (section by section)
- ✅ No new features introduced
- ✅ Describes HOW, not WHAT
- ✅ Testable architecture
- ✅ Clear separation of concerns
- ✅ Phase II migration path documented

---

**Document Status**: 🟢 READY FOR APPROVAL

**Next Steps After Approval**:
1. User approves this plan
2. Create `phase-1-core-console-app/tasks.md` (testable work breakdown)
3. Begin Red-Green-Refactor implementation cycle
4. Write failing tests first (Red phase)
5. Implement to pass tests (Green phase)
6. Refactor with tests passing (Refactor phase)

---

**Version**: 1.0.0 | **Date**: 2025-12-30 | **Status**: Pending User Approval
