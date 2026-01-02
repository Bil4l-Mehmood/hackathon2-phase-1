# Phase I: Core Console Todo Application - Task Breakdown

**Version**: 1.0.0 | **Date**: 2025-12-30 | **Phase**: I (Foundation)

**Constitutional Alignment**: ✅ Complies with EVOLUTION_CONSTITUTION.md Part I (Spec-Driven), Part VI (Development Workflow)

**References**:
- **Specification**: `phase-1-core-console-app/spec.md`
- **Architecture Plan**: `phase-1-core-console-app/plan.md`

---

## Overview

This document breaks Phase I implementation into atomic, testable tasks. Each task:
- Is independently testable
- Has clear preconditions and outputs
- References specification and plan sections
- Does not introduce new features
- Does not reference future phases

**Implementation Approach**: Red-Green-Refactor (write failing tests → implement → refactor)

---

## Task Dependency Graph

```
TASK-001: Exception Classes
    ↓
TASK-002: Task Data Model
    ├─→ TASK-003: TaskStatus Enum (parallel with 002)
    ↓
TASK-004: TaskRepository
    ├─→ TASK-005: Repository ID Generation (parallel with 004)
    ↓
TASK-006: Input Validators (Service Layer)
    ↓
TASK-007: Task Service - CRUD
    ├─→ TASK-008: Task Service - Status Operations (parallel with 007)
    ↓
TASK-009: CLI Infrastructure
    ├─→ TASK-010: Menu Display (parallel with 009)
    ├─→ TASK-011: Input Helpers (parallel with 009)
    ↓
TASK-012: Add Task Flow
    ↓
TASK-013: View Tasks Flow
    ↓
TASK-014: Update Task Flow
    ↓
TASK-015: Delete Task Flow
    ↓
TASK-016: Toggle Status Flow
    ↓
TASK-017: Application Entry Point
    ↓
TASK-018: Integration Tests
    ↓
TASK-019: Code Review & Coverage Verification
```

---

## Phase I Tasks

---

### TASK-001: Define Custom Exception Classes

**Task ID**: 001
**Title**: Create exception class hierarchy

**Description**:
Create custom exception classes for Phase I error handling. These exceptions are raised by the service layer and caught by the CLI layer to display user-friendly error messages.

**Preconditions**:
- None (foundational task)

**Specification References**:
- Spec §6: Error Cases & Handling
- Spec §6 Error Taxonomy

**Plan References**:
- Plan §8: Error Handling Strategy
- Plan §8.1: Exception Hierarchy

**Expected Output**:
1. File `app/exceptions.py` created
2. Exception class hierarchy defined:
   - `TodoAppException` (base exception)
   - `ValidationError` (input/logic validation errors)
   - `TaskNotFoundError` (task ID doesn't exist)

**Artifacts to Create**:
- `app/exceptions.py`

**Test Cases**:
- [x] Can import TodoAppException
- [x] Can import ValidationError
- [x] Can import TaskNotFoundError
- [x] ValidationError inherits from TodoAppException
- [x] TaskNotFoundError inherits from TodoAppException
- [x] Can raise and catch each exception type
- [x] Exception message preserved when raised

**Success Criteria**:
```python
# Can create and raise exceptions
try:
    raise ValidationError("Task title cannot be empty")
except ValidationError as e:
    assert str(e) == "Task title cannot be empty"

# Can distinguish exception types
try:
    raise TaskNotFoundError("Task ID 99 not found")
except TaskNotFoundError:
    pass  # Caught successfully
```

---

### TASK-002: Implement Task Domain Model

**Task ID**: 002
**Title**: Create Task entity class with immutable ID

**Description**:
Implement the core Task domain entity with all required fields and methods. The Task represents a single todo item with immutable ID and mutable title, description, and status.

**Preconditions**:
- TASK-001 completed (exceptions available)

**Specification References**:
- Spec §3: Task Data Model
- Spec §3.1: Task Entity
- Spec §3 Data Constraints (all fields)

**Plan References**:
- Plan §3: Domain Layer: Task Entity
- Plan §3.1: Task Model Class
- Plan §3.2: Task Constraints

**Expected Output**:
1. File `app/models.py` created
2. Task class with:
   - Constructor: `__init__(task_id, title, description, status, created_at)`
   - Properties: id, title, description, status, created_at
   - Methods: update_title(), update_description(), mark_complete(), mark_incomplete(), is_complete()
3. All fields match specification exactly

**Artifacts to Create**:
- `app/models.py`

**Test Cases**:
- [x] Task created with title only (description defaults to empty)
- [x] Task created with title and description
- [x] Task ID is immutable (cannot be changed after creation)
- [x] Task status defaults to INCOMPLETE
- [x] Task created_at defaults to current time (ISO 8601)
- [x] Task.update_title() changes title
- [x] Task.update_description() changes description
- [x] Task.mark_complete() sets status to COMPLETE
- [x] Task.mark_incomplete() sets status to INCOMPLETE
- [x] Task.is_complete() returns True for COMPLETE, False for INCOMPLETE
- [x] Task has string representation (__repr__)

**Success Criteria**:
```python
from datetime import datetime
from models import Task, TaskStatus

# Create task with title only
task = Task(task_id=1, title="Buy groceries")
assert task.id == 1
assert task.title == "Buy groceries"
assert task.description == ""
assert task.status == TaskStatus.INCOMPLETE
assert isinstance(task.created_at, datetime)

# Update task
task.update_title("Get groceries")
assert task.title == "Get groceries"

# Change status
task.mark_complete()
assert task.is_complete() == True
assert task.status == TaskStatus.COMPLETE

task.mark_incomplete()
assert task.is_complete() == False
```

---

### TASK-003: Create TaskStatus Enum

**Task ID**: 003
**Title**: Define TaskStatus enumeration

**Description**:
Create an enumeration for task status values. This ensures type-safe status representation instead of string-based statuses.

**Preconditions**:
- None (can parallel with TASK-002)

**Specification References**:
- Spec §3.3: Task Status Enum

**Plan References**:
- Plan §3.1: Task Model Class (uses TaskStatus)
- Plan §10.4: Enum for Status (design pattern)

**Expected Output**:
1. File `app/models.py` updated (or created if part of TASK-002)
2. TaskStatus enum with two values:
   - INCOMPLETE: "incomplete"
   - COMPLETE: "complete"

**Artifacts to Create/Modify**:
- `app/models.py`

**Test Cases**:
- [x] TaskStatus.INCOMPLETE exists
- [x] TaskStatus.COMPLETE exists
- [x] TaskStatus.INCOMPLETE.value == "incomplete"
- [x] TaskStatus.COMPLETE.value == "complete"
- [x] Can compare TaskStatus values
- [x] Cannot create invalid TaskStatus values

**Success Criteria**:
```python
from models import TaskStatus

assert TaskStatus.INCOMPLETE.value == "incomplete"
assert TaskStatus.COMPLETE.value == "complete"

status = TaskStatus.INCOMPLETE
assert status == TaskStatus.INCOMPLETE
assert status != TaskStatus.COMPLETE
```

---

### TASK-004: Implement TaskRepository Class

**Task ID**: 004
**Title**: Create in-memory task storage with repository pattern

**Description**:
Implement the TaskRepository class that manages in-memory task storage using a Python dictionary. Handles task persistence (storage/retrieval) and ID generation state.

**Preconditions**:
- TASK-002 completed (Task model available)

**Specification References**:
- Spec §3.4: In-Memory Storage (Dict[int, Task])
- Spec §3.3: Task ID Generation (sequential, starting at 1)

**Plan References**:
- Plan §4: In-Memory Data Structures
- Plan §4.1: TaskRepository Class
- Plan §4.2: Data Structure Design Rationale

**Expected Output**:
1. File `app/repository.py` created
2. TaskRepository class with:
   - Constructor: `__init__()` initializes empty dict and next_id=1
   - Methods: add_task(), get_task(), get_all_tasks(), delete_task(), task_exists(), get_next_id(), clear()
   - Internal state: _tasks (dict), _next_id (int)

**Artifacts to Create**:
- `app/repository.py`

**Test Cases**:
- [x] Repository created empty
- [x] Repository initial next_id is 1
- [x] add_task(task) stores task in dict
- [x] get_task(id) retrieves task by ID
- [x] get_task(id) returns None for non-existent ID
- [x] get_all_tasks() returns empty list when empty
- [x] get_all_tasks() returns all tasks sorted by ID
- [x] delete_task(id) removes task from storage
- [x] delete_task(id) returns True if deleted, False if not found
- [x] task_exists(id) returns True for existing tasks
- [x] task_exists(id) returns False for non-existent tasks
- [x] get_next_id() returns correct ID
- [x] After adding task, get_next_id() increments
- [x] clear() empties all tasks and resets next_id to 1

**Success Criteria**:
```python
from repository import TaskRepository
from models import Task

repo = TaskRepository()
assert repo.get_next_id() == 1
assert repo.get_all_tasks() == []

# Add task
task = Task(task_id=1, title="Test")
repo.add_task(task)
assert repo.task_exists(1) == True
assert repo.get_task(1) == task
assert len(repo.get_all_tasks()) == 1
assert repo.get_next_id() == 2

# Delete task
assert repo.delete_task(1) == True
assert repo.task_exists(1) == False
assert repo.get_all_tasks() == []
```

---

### TASK-005: Implement Sequential ID Generation

**Task ID**: 005
**Title**: Create sequential ID generation strategy

**Description**:
Implement ID generation in the repository. IDs start at 1, increment sequentially, and are never reused even after deletion (gaps are allowed).

**Preconditions**:
- TASK-004 completed (TaskRepository exists)

**Specification References**:
- Spec §3.3: Task ID Generation (sequential, starting at 1, never reused, max-based)

**Plan References**:
- Plan §5: Task Identification Strategy
- Plan §5.1: ID Generation Algorithm
- Plan §5.2: Implementation Example

**Expected Output**:
1. File `app/repository.py` updated
2. Method `create_task_id()` returns next available ID
3. Method updates _next_id automatically after ID assignment
4. ID gaps allowed after deletion (next_id doesn't decrement)

**Artifacts to Modify**:
- `app/repository.py`

**Test Cases**:
- [x] First ID is 1
- [x] Each subsequent call increments ID by 1
- [x] After deletion, next ID continues from max+1 (no reuse)
- [x] ID assignment: create_task_id() → 1, 2, 3, then delete 2 → next is 4

**Success Criteria**:
```python
repo = TaskRepository()

# Generate IDs
id1 = repo.get_next_id()  # 1
task1 = Task(id1, "Task 1")
repo.add_task(task1)

id2 = repo.get_next_id()  # 2
task2 = Task(id2, "Task 2")
repo.add_task(task2)

id3 = repo.get_next_id()  # 3
task3 = Task(id3, "Task 3")
repo.add_task(task3)

# Delete middle task
repo.delete_task(2)

# Next ID continues from max, not reusing 2
id4 = repo.get_next_id()  # 4 (not 2)
assert id4 == 4
```

---

### TASK-006: Implement Input Validators in Service Layer

**Task ID**: 006
**Title**: Create service-layer validation for task data

**Description**:
Implement validation methods in the TaskService class that validate task title, description, and task ID. These validators raise appropriate exceptions for invalid input.

**Preconditions**:
- TASK-001 completed (exceptions available)
- TASK-004 completed (TaskRepository available)

**Specification References**:
- Spec §4: CLI Interaction Flow (User Input Validation)
- Spec §3 Data Constraints (field lengths, requirements)
- Spec §6 Error Cases & Handling (error messages, validation)

**Plan References**:
- Plan §6: Service Layer: Task Operations
- Plan §6.1: TaskService Class (validation methods)

**Expected Output**:
1. File `app/service.py` created with TaskService class
2. Methods:
   - `validate_title(title)` → raises ValidationError for invalid titles
   - `validate_description(description)` → raises ValidationError for invalid descriptions
   - `validate_task_id(task_id)` → raises TaskNotFoundError if task doesn't exist
3. Validation logic matches specification exactly

**Artifacts to Create**:
- `app/service.py`

**Test Cases**:
- [x] validate_title() accepts "Buy groceries"
- [x] validate_title() rejects empty string with error
- [x] validate_title() rejects whitespace-only string with error
- [x] validate_title() rejects string > 200 chars with error
- [x] validate_title() trims whitespace
- [x] validate_description() accepts empty string (optional)
- [x] validate_description() accepts valid description
- [x] validate_description() rejects string > 500 chars with error
- [x] validate_description() trims whitespace
- [x] validate_task_id() accepts valid task ID (that exists)
- [x] validate_task_id() raises TaskNotFoundError for non-existent ID
- [x] Error messages match specification exactly

**Success Criteria**:
```python
from service import TaskService
from repository import TaskRepository
from exceptions import ValidationError, TaskNotFoundError

repo = TaskRepository()
service = TaskService(repo)

# Title validation
try:
    service.validate_title("")
    assert False, "Should raise ValidationError"
except ValidationError as e:
    assert "cannot be empty" in str(e).lower()

try:
    service.validate_title("x" * 201)
    assert False, "Should raise ValidationError"
except ValidationError as e:
    assert "exceeds 200" in str(e).lower()

# Description validation
desc = service.validate_description("")
assert desc == ""

# Task ID validation
try:
    service.validate_task_id(99)
    assert False, "Should raise TaskNotFoundError"
except TaskNotFoundError:
    pass
```

---

### TASK-007: Implement Task Service - CRUD Operations

**Task ID**: 007
**Title**: Create service layer CRUD operations

**Description**:
Implement CRUD (Create, Read, Update, Delete) operations in TaskService. These methods validate input, call repository methods, and handle business logic.

**Preconditions**:
- TASK-006 completed (validators available)
- TASK-004 completed (TaskRepository available)
- TASK-002 completed (Task model available)

**Specification References**:
- Spec §2: User Stories 1-4 (Add, View, Update, Delete)
- Spec §5: Acceptance Criteria by Feature (criteria for each CRUD operation)

**Plan References**:
- Plan §6.1: TaskService Class (CRUD methods)
- Plan §6: Service Layer: Task Operations

**Expected Output**:
1. File `app/service.py` updated
2. Methods:
   - `add_task(title, description)` → creates Task with validated inputs
   - `get_all_tasks()` → returns list sorted by ID
   - `get_task(task_id)` → returns Task or raises TaskNotFoundError
   - `update_task(task_id, new_title, new_description)` → updates Task fields
   - `delete_task(task_id)` → removes Task and returns it

**Artifacts to Modify**:
- `app/service.py`

**Test Cases**:

**Add Task**:
- [x] add_task("Buy milk") creates task with ID 1
- [x] add_task("Task", "Desc") creates task with both fields
- [x] Created task defaults to INCOMPLETE
- [x] Task is immediately accessible via get_task()
- [x] add_task() raises ValidationError for empty title
- [x] add_task() raises ValidationError for long title

**Get All Tasks**:
- [x] get_all_tasks() returns empty list when no tasks
- [x] get_all_tasks() returns all tasks sorted by ID
- [x] Tasks returned in ascending ID order (even if added out of order)

**Get Task**:
- [x] get_task(1) returns task with ID 1
- [x] get_task(99) raises TaskNotFoundError
- [x] Error message includes task ID

**Update Task**:
- [x] update_task(id, "New Title", None) updates title only
- [x] update_task(id, None, "New Desc") updates description only
- [x] update_task(id, "New Title", "New Desc") updates both
- [x] update_task(id, None, None) returns no change indicator
- [x] update_task() validates new title
- [x] update_task() validates new description
- [x] Task ID never changes
- [x] Task status never changes via update
- [x] update_task() returns (updated_task, was_changed)

**Delete Task**:
- [x] delete_task(1) removes task
- [x] Deleted task is no longer accessible
- [x] delete_task() returns deleted Task for confirmation
- [x] delete_task() raises TaskNotFoundError for non-existent ID
- [x] Other tasks remain unchanged after deletion

**Success Criteria**:
```python
from service import TaskService
from repository import TaskRepository

repo = TaskRepository()
service = TaskService(repo)

# Add tasks
task1 = service.add_task("Task 1")
task2 = service.add_task("Task 2", "Description")
assert task1.id == 1
assert task2.id == 2
assert task2.description == "Description"

# View all
all_tasks = service.get_all_tasks()
assert len(all_tasks) == 2
assert all_tasks[0].id == 1
assert all_tasks[1].id == 2

# Update
updated, changed = service.update_task(1, "New Title", None)
assert changed == True
assert updated.title == "New Title"
assert updated.status == TaskStatus.INCOMPLETE  # unchanged

# Delete
deleted = service.delete_task(1)
assert deleted.id == 1
assert len(service.get_all_tasks()) == 1
```

---

### TASK-008: Implement Task Service - Status Operations

**Task ID**: 008
**Title**: Create task status transition methods

**Description**:
Implement status transition methods (mark_complete, mark_incomplete) in TaskService. These methods validate state transitions (cannot mark already-complete as complete, etc.).

**Preconditions**:
- TASK-007 completed (CRUD operations available)
- TASK-003 completed (TaskStatus enum)

**Specification References**:
- Spec §2: User Story 5 (Mark Task Complete/Incomplete)
- Spec §5: Feature 5 Acceptance Criteria (status transition rules)

**Plan References**:
- Plan §6.1: TaskService Class (status methods)

**Expected Output**:
1. File `app/service.py` updated
2. Methods:
   - `mark_complete(task_id)` → transitions to COMPLETE or raises error
   - `mark_incomplete(task_id)` → transitions to INCOMPLETE or raises error
   - `get_statistics()` → returns (total, completed, remaining)

**Artifacts to Modify**:
- `app/service.py`

**Test Cases**:
- [x] mark_complete(id) changes INCOMPLETE → COMPLETE
- [x] mark_complete(id) raises ValidationError if already complete
- [x] mark_incomplete(id) changes COMPLETE → INCOMPLETE
- [x] mark_incomplete(id) raises ValidationError if already incomplete
- [x] mark_complete(id) raises TaskNotFoundError for non-existent ID
- [x] mark_incomplete(id) raises TaskNotFoundError for non-existent ID
- [x] Status transitions preserve title and description
- [x] get_statistics() returns correct counts
- [x] get_statistics() counts total, completed, remaining tasks

**Success Criteria**:
```python
service = TaskService(repo)
task = service.add_task("Test task")

# Initially incomplete
assert task.is_complete() == False

# Mark complete
completed_task = service.mark_complete(task.id)
assert completed_task.is_complete() == True

# Cannot mark complete again
try:
    service.mark_complete(task.id)
    assert False, "Should raise ValidationError"
except ValidationError:
    pass

# Mark incomplete
incomplete_task = service.mark_incomplete(task.id)
assert incomplete_task.is_complete() == False

# Statistics
service.add_task("Task 2")
service.add_task("Task 3")
service.mark_complete(1)
service.mark_complete(3)

total, completed, remaining = service.get_statistics()
assert total == 3
assert completed == 2
assert remaining == 1
```

---

### TASK-009: Create CLI Infrastructure and Application Class

**Task ID**: 009
**Title**: Set up TodoApp class and CLI framework

**Description**:
Create the main TodoApp class that coordinates the CLI interface. Initialize repository and service. Implement the main application loop structure (show menu, get input, execute action, loop).

**Preconditions**:
- TASK-007 completed (TaskService available)
- TASK-004 completed (TaskRepository available)

**Plan References**:
- Plan §7: CLI Control Flow
- Plan §7.1: CLI Architecture
- Plan §7.2: Menu Loop Design

**Expected Output**:
1. File `app/ui.py` created
2. TodoApp class with:
   - Constructor: initializes repository, service, displays welcome
   - Method `run()` implements main application loop
   - Main loop: display menu → get input → execute action → handle errors → repeat
   - Error handling catches ValidationError and TaskNotFoundError

**Artifacts to Create**:
- `app/ui.py`

**Test Cases**:
- [x] TodoApp can be instantiated
- [x] TodoApp creates repository and service
- [x] TodoApp can call run() method
- [x] Main loop handles user exit (choice 6)
- [x] Main loop catches ValidationError and displays message
- [x] Main loop catches TaskNotFoundError and displays message
- [x] Main loop returns to menu after errors

**Success Criteria**:
```python
# Can instantiate and verify structure
app = TodoApp()
assert app.service is not None
assert app.repo is not None

# Verify main components exist
assert hasattr(app, 'run')
assert hasattr(app, 'show_menu')
assert hasattr(app, 'execute_action')
```

---

### TASK-010: Implement Menu Display and Input Handling

**Task ID**: 010
**Title**: Create menu display and choice validation

**Description**:
Implement menu display and user input handling. Display main menu with all 6 options. Validate menu selection (must be 1-6 numeric). Show error messages for invalid selections.

**Preconditions**:
- TASK-009 completed (TodoApp class exists)

**Plan References**:
- Plan §7.1: CLI Architecture (show_menu)
- Plan §7.2: Menu Loop Design (menu validation)

**Specification References**:
- Spec §4: CLI Interaction Flow (Main Menu)
- Spec §4.3: User Input Validation (Menu Selection)

**Expected Output**:
1. File `app/ui.py` updated
2. Methods:
   - `show_menu()` displays menu with 6 options
   - `get_menu_choice()` validates input is 1-6 numeric
   - Invalid input shows error and retries
   - Menu options: Add, View, Update, Delete, Toggle, Exit

**Artifacts to Modify**:
- `app/ui.py`

**Test Cases**:
- [x] show_menu() displays all 6 options
- [x] Menu shows correct text for each option
- [x] get_menu_choice() accepts valid input 1-6
- [x] get_menu_choice() rejects non-numeric input
- [x] get_menu_choice() rejects values outside 1-6
- [x] get_menu_choice() shows error for invalid input
- [x] get_menu_choice() retries on invalid input

**Success Criteria**:
```
Menu display includes:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Error messages for invalid input:
- Non-numeric: "Error: Please enter a number between 1 and 6"
- Out of range: "Error: Please enter a number between 1 and 6"
```

---

### TASK-011: Implement CLI Input Helpers

**Task ID**: 011
**Title**: Create input validation helper methods

**Description**:
Implement reusable input helper methods for the CLI layer. These methods handle getting text, numeric, and confirmation input with validation.

**Preconditions**:
- TASK-009 completed (TodoApp class exists)
- TASK-001 completed (exceptions available)

**Plan References**:
- Plan §7.1: CLI Architecture (input helpers)

**Specification References**:
- Spec §4.3: User Input Validation (all input patterns)

**Expected Output**:
1. File `app/ui.py` updated
2. Methods:
   - `get_text_input(prompt, required, max_length)` → validates text input
   - `get_numeric_input(prompt)` → validates numeric input
   - `get_confirmation()` → validates y/n response
3. All methods show error messages and retry on invalid input

**Artifacts to Modify**:
- `app/ui.py`

**Test Cases**:
- [x] get_text_input() accepts valid text
- [x] get_text_input(required=True) rejects empty input
- [x] get_text_input(required=False) accepts empty input
- [x] get_text_input(max_length=5) rejects longer input
- [x] get_numeric_input() accepts numeric input
- [x] get_numeric_input() rejects non-numeric input
- [x] get_numeric_input() shows error for non-numeric
- [x] get_confirmation() accepts 'y' and 'yes'
- [x] get_confirmation() accepts 'n' and 'no'
- [x] get_confirmation() case-insensitive
- [x] get_confirmation() rejects invalid responses

**Success Criteria**:
- Text input validation works correctly
- Numeric input parsing works correctly
- Confirmation accepts y/n variants
- All methods retry on error

---

### TASK-012: Implement Add Task Flow

**Task ID**: 012
**Title**: Create add task user interaction flow

**Description**:
Implement the complete user flow for adding a task. Prompt user for title and optional description. Validate inputs. Create task. Display confirmation with new task ID.

**Preconditions**:
- TASK-007 completed (add_task service method)
- TASK-011 completed (input helpers)
- TASK-009 completed (TodoApp class)

**Specification References**:
- Spec §2: User Story 1 (Add a New Task)
- Spec §5: Feature 1 Acceptance Criteria

**Plan References**:
- Plan §7.1: CLI Architecture (action_add_task method)

**Expected Output**:
1. File `app/ui.py` updated
2. Method `action_add_task()` implements flow:
   - Prompt for task title (required)
   - Prompt for task description (optional)
   - Call service.add_task()
   - Display confirmation with task ID
   - Handle errors (ValidationError)

**Artifacts to Modify**:
- `app/ui.py`

**Test Cases**:
- [x] User can enter task title
- [x] User can enter optional description
- [x] Task created with auto-generated ID
- [x] Confirmation shows task ID
- [x] Empty title rejected with error message
- [x] Long title rejected with error message
- [x] Long description rejected with error message
- [x] Returns to menu after completion
- [x] Returns to menu after error

**Success Criteria**:
```
User Flow:
1. Menu: > [1] Add Task
2. Enter task title: "Buy groceries"
3. Enter task description (press Enter to skip): "Milk, eggs, bread"
4. Output: "✓ Task created with ID: 1"
5. Output: "Task: "Buy groceries" [incomplete]"
```

---

### TASK-013: Implement View Tasks Flow

**Task ID**: 013
**Title**: Create view task list display

**Description**:
Implement the user flow for viewing all tasks. Display tasks in a formatted table with ID, Status, Title, and Description. Show task count summary. Handle empty list.

**Preconditions**:
- TASK-008 completed (get_all_tasks, get_statistics)
- TASK-009 completed (TodoApp class)

**Specification References**:
- Spec §2: User Story 2 (View Task List)
- Spec §5: Feature 2 Acceptance Criteria

**Plan References**:
- Plan §7.1: CLI Architecture (action_view_tasks method)

**Expected Output**:
1. File `app/ui.py` updated
2. Method `action_view_tasks()` implements flow:
   - Call service.get_all_tasks()
   - Format tasks in readable table
   - Show task count summary
   - Handle empty list (display "No tasks yet")

**Artifacts to Modify**:
- `app/ui.py`

**Test Cases**:
- [x] Empty list shows "No tasks yet"
- [x] Tasks displayed in ID order (ascending)
- [x] Each task shows: ID, Status (✓/○), Title, Description
- [x] Status symbol correct (✓ for complete, ○ for incomplete)
- [x] Description shows "(no description)" if empty
- [x] Summary line shows total, completed, remaining counts
- [x] Table is readable and well-formatted

**Success Criteria**:
```
Display format:
ID | Status | Title          | Description
---+--------+----------------+-------------------
1  | ○      | Buy groceries  | Milk, eggs, bread
2  | ✓      | Call dentist   | (no description)
---+--------+----------------+-------------------
Total: 2 tasks | Completed: 1 | Remaining: 1
```

---

### TASK-014: Implement Update Task Flow

**Task ID**: 014
**Title**: Create update task user interaction flow

**Description**:
Implement the user flow for updating a task. Prompt for task ID. Display current task. Prompt for new title and description (both optional). Update task. Show confirmation.

**Preconditions**:
- TASK-007 completed (update_task service method)
- TASK-011 completed (input helpers)
- TASK-009 completed (TodoApp class)

**Specification References**:
- Spec §2: User Story 3 (Update Task)
- Spec §5: Feature 3 Acceptance Criteria

**Plan References**:
- Plan §7.1: CLI Architecture (action_update_task method)

**Expected Output**:
1. File `app/ui.py` updated
2. Method `action_update_task()` implements flow:
   - Get task ID from user (numeric, must exist)
   - Display current task details
   - Prompt for new title (optional, press Enter to skip)
   - Prompt for new description (optional, press Enter to skip)
   - Call service.update_task()
   - Show confirmation with updated details or "no changes" message
   - Handle errors (TaskNotFoundError, ValidationError)

**Artifacts to Modify**:
- `app/ui.py`

**Test Cases**:
- [x] User can select task by ID
- [x] Current task details displayed
- [x] User can update title only
- [x] User can update description only
- [x] User can update both
- [x] User can skip updates (no change)
- [x] Non-existent task ID shows error
- [x] Non-numeric ID shows error
- [x] Invalid title (too long) shows error
- [x] Confirmation shows updated task
- [x] "No changes made" message when no updates
- [x] Returns to menu after completion

**Success Criteria**:
```
User Flow:
1. Menu: > [3] Update Task
2. Enter task ID to update: 1
3. Current task: "Buy groceries" (Milk, eggs, bread)
4. Enter new title (press Enter to keep current): "Get groceries"
5. Enter new description (press Enter to keep current):
6. Output: "✓ Task 1 updated successfully"
7. Output: "Updated task: "Get groceries" (Milk, eggs, bread)"
```

---

### TASK-015: Implement Delete Task Flow

**Task ID**: 015
**Title**: Create delete task user interaction flow

**Description**:
Implement the user flow for deleting a task. Prompt for task ID. Display task details. Ask for confirmation (y/n). Delete if confirmed. Show confirmation message.

**Preconditions**:
- TASK-007 completed (delete_task service method)
- TASK-011 completed (input helpers)
- TASK-009 completed (TodoApp class)

**Specification References**:
- Spec §2: User Story 4 (Delete Task)
- Spec §5: Feature 4 Acceptance Criteria

**Plan References**:
- Plan §7.1: CLI Architecture (action_delete_task method)

**Expected Output**:
1. File `app/ui.py` updated
2. Method `action_delete_task()` implements flow:
   - Get task ID from user (numeric, must exist)
   - Display task to be deleted
   - Ask for y/n confirmation
   - Delete only if confirmed (y)
   - Show "deleted" or "cancelled" message
   - Handle errors (TaskNotFoundError, ValidationError)

**Artifacts to Modify**:
- `app/ui.py`

**Test Cases**:
- [x] User can select task by ID
- [x] Task details shown before confirmation
- [x] Confirmation prompt shows task
- [x] Delete confirmed with 'y'
- [x] Delete confirmed with 'yes'
- [x] Deletion cancelled with 'n'
- [x] Deletion cancelled with 'no'
- [x] Non-existent task ID shows error
- [x] Non-numeric ID shows error
- [x] Invalid confirmation response retries
- [x] Deleted task no longer in list
- [x] Other tasks unchanged
- [x] Returns to menu after completion

**Success Criteria**:
```
User Flow (Delete Confirmed):
1. Menu: > [4] Delete Task
2. Enter task ID to delete: 1
3. Delete task? "Buy groceries" (Milk, eggs, bread)
4. Confirm? (y/n): y
5. Output: "✓ Task 1 deleted successfully"

User Flow (Delete Cancelled):
1. Menu: > [4] Delete Task
2. Enter task ID to delete: 1
3. Delete task? "Buy groceries" (Milk, eggs, bread)
4. Confirm? (y/n): n
5. Output: "Deletion cancelled. Task remains"
```

---

### TASK-016: Implement Toggle Task Status Flow

**Task ID**: 016
**Title**: Create mark complete/incomplete user interaction flow

**Description**:
Implement the user flow for toggling task status (complete ↔ incomplete). Prompt for task ID. Display current status. Show options (1: Mark Complete, 2: Mark Incomplete). Execute selected action. Show confirmation.

**Preconditions**:
- TASK-008 completed (mark_complete, mark_incomplete)
- TASK-011 completed (input helpers)
- TASK-009 completed (TodoApp class)

**Specification References**:
- Spec §2: User Story 5 (Mark Task Complete/Incomplete)
- Spec §5: Feature 5 Acceptance Criteria

**Plan References**:
- Plan §7.1: CLI Architecture (action_toggle_status method)

**Expected Output**:
1. File `app/ui.py` updated
2. Method `action_toggle_status()` implements flow:
   - Get task ID from user (numeric, must exist)
   - Display current task status
   - Show options: 1) Mark Complete, 2) Mark Incomplete
   - Get user choice (1 or 2)
   - Call mark_complete() or mark_incomplete()
   - Show new status
   - Handle errors (TaskNotFoundError, ValidationError)

**Artifacts to Modify**:
- `app/ui.py`

**Test Cases**:
- [x] User can select task by ID
- [x] Current status displayed (✓ or ○)
- [x] Options shown (1: Complete, 2: Incomplete)
- [x] User selects option 1 to mark complete
- [x] User selects option 2 to mark incomplete
- [x] Cannot mark already-complete as complete (error)
- [x] Cannot mark already-incomplete as incomplete (error)
- [x] Non-existent task ID shows error
- [x] Non-numeric ID shows error
- [x] Invalid choice (not 1-2) retries
- [x] Confirmation shows new status
- [x] Returns to menu after completion

**Success Criteria**:
```
User Flow (Mark Complete):
1. Menu: > [5] Mark Task Complete/Incomplete
2. Enter task ID: 1
3. Current status: ○ incomplete
4. Options:
   1. Mark Complete
   2. Mark Incomplete
5. Choose (1-2): 1
6. Output: "✓ Task 1 marked as complete"
7. Output: "New status: ✓ complete"

User Flow (Mark Incomplete):
1. Menu: > [5] Mark Task Complete/Incomplete
2. Enter task ID: 1
3. Current status: ✓ complete
4. Options:
   1. Mark Complete
   2. Mark Incomplete
5. Choose (1-2): 2
6. Output: "✓ Task 1 marked as incomplete"
7. Output: "New status: ○ incomplete"
```

---

### TASK-017: Implement Application Entry Point

**Task ID**: 017
**Title**: Create main.py entry point and application startup

**Description**:
Create the main entry point (main.py) that starts the application. Initialize TodoApp and call run() method. Handle graceful shutdown.

**Preconditions**:
- TASK-009 completed (TodoApp class)

**Plan References**:
- Plan §2.3: Execution Flow
- Plan §2.1: Application Architecture Diagram

**Expected Output**:
1. File `app/main.py` created
2. `if __name__ == "__main__"` entry point
3. Creates TodoApp instance
4. Calls app.run()
5. Handles KeyboardInterrupt gracefully
6. Can be run directly: `python app/main.py`

**Artifacts to Create**:
- `app/main.py`
- `app/__init__.py` (empty package file)

**Test Cases**:
- [x] main.py can be imported
- [x] main.py has `if __name__ == "__main__"` block
- [x] Entry point creates TodoApp
- [x] Entry point calls app.run()
- [x] Application starts without errors
- [x] Application can be exited cleanly

**Success Criteria**:
```bash
# Can run application
$ python app/main.py
========== TODO APPLICATION ==========
[Menu displays and application runs]
```

---

### TASK-018: Create Comprehensive Integration Tests

**Task ID**: 018
**Title**: Write end-to-end workflow tests

**Description**:
Write integration tests that exercise complete user workflows across multiple features. Test full scenarios: add tasks, view, update, delete, toggle status.

**Preconditions**:
- TASK-012 through TASK-016 completed (all features)

**Plan References**:
- Plan §13: Testing Architecture

**Expected Output**:
1. File `tests/test_integration.py` created
2. Test classes/functions covering workflows:
   - Add → View (task appears)
   - Add → Update → View (changes reflected)
   - Add → Delete → View (task disappears)
   - Add → Mark Complete → View (status updated)
   - Complex workflow: multiple adds, updates, deletes, toggles

**Artifacts to Create**:
- `tests/test_integration.py`

**Test Cases**:
- [x] Add single task and view
- [x] Add multiple tasks and view order
- [x] Add → Update → View workflow
- [x] Add → Delete → View workflow
- [x] Add → Mark Complete → View workflow
- [x] Complex workflow (multiple operations)
- [x] Error handling in workflows

**Success Criteria**:
```python
# Example integration test
def test_complete_workflow():
    service = TaskService(TaskRepository())

    # Add tasks
    t1 = service.add_task("Task 1")
    t2 = service.add_task("Task 2")

    # View
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 2

    # Update
    service.update_task(t1.id, "Updated Task 1", None)

    # Mark complete
    service.mark_complete(t1.id)

    # Delete
    service.delete_task(t2.id)

    # Verify final state
    final = service.get_all_tasks()
    assert len(final) == 1
    assert final[0].id == t1.id
    assert final[0].is_complete()
```

---

### TASK-019: Code Review and Coverage Verification

**Task ID**: 019
**Title**: Final code review and test coverage verification

**Description**:
Review all code for quality, consistency, and compliance. Verify test coverage meets 80% minimum. Verify all acceptance criteria met. Prepare for Phase II transition.

**Preconditions**:
- TASK-018 completed (all features implemented and tested)

**Expected Output**:
1. Code review checklist:
   - [ ] All code follows PEP 8 style
   - [ ] All functions have docstrings
   - [ ] All modules properly organized
   - [ ] No unused imports or variables
   - [ ] Clean architecture layers respected
   - [ ] Separation of concerns maintained

2. Test coverage verification:
   - [ ] Unit tests: 100% coverage for critical code
   - [ ] Integration tests: Complete workflow coverage
   - [ ] Overall: 80%+ coverage minimum
   - [ ] All error cases tested

3. Specification compliance:
   - [ ] All 5 user stories implemented
   - [ ] All acceptance criteria met
   - [ ] All error cases handled
   - [ ] Data model matches specification
   - [ ] CLI flows match specification

4. Plan compliance:
   - [ ] Four-layer architecture implemented
   - [ ] Clean separation of concerns
   - [ ] Dependency flow correct (no upward deps)
   - [ ] Error handling strategy followed
   - [ ] ID generation matches plan

**Artifacts to Verify**:
- All source files (app/*.py)
- All test files (tests/test_*.py)
- requirements.txt
- README.md

**Verification Checklist**:
- [x] Code quality checks
- [x] Test coverage meets target
- [x] Specification compliance
- [x] Plan compliance
- [x] No Phase II concepts
- [x] Ready for production

**Success Criteria**:
```
Code Quality:
- PEP 8 compliant
- 100% docstring coverage
- Clean imports
- No code duplication

Test Coverage:
- models.py: 100%
- repository.py: 100%
- service.py: 100%
- ui.py: 80%+
- Overall: 80%+

Feature Completion:
- Add Task: ✓
- View Tasks: ✓
- Update Task: ✓
- Delete Task: ✓
- Toggle Status: ✓
- Error Handling: ✓
- All acceptance criteria: ✓
```

---

## Task Summary Table

| ID | Title | Dependencies | Priority |
|----|-------|--------------|----------|
| 001 | Exception Classes | None | Critical |
| 002 | Task Data Model | 001 | Critical |
| 003 | TaskStatus Enum | None | Critical |
| 004 | TaskRepository | 002 | Critical |
| 005 | ID Generation | 004 | Critical |
| 006 | Input Validators | 001, 004 | High |
| 007 | CRUD Operations | 006 | High |
| 008 | Status Operations | 007, 003 | High |
| 009 | CLI Infrastructure | 007, 004 | High |
| 010 | Menu Display | 009 | High |
| 011 | Input Helpers | 009, 001 | High |
| 012 | Add Task Flow | 007, 011, 009 | High |
| 013 | View Tasks Flow | 008, 009 | High |
| 014 | Update Task Flow | 007, 011, 009 | High |
| 015 | Delete Task Flow | 007, 011, 009 | High |
| 016 | Toggle Status Flow | 008, 011, 009 | High |
| 017 | Entry Point | 009 | Medium |
| 018 | Integration Tests | 012-016 | High |
| 019 | Code Review | All | Medium |

---

## Development Workflow

For each task, follow Red-Green-Refactor:

### RED Phase: Write Failing Tests
1. Create test file (or add to existing test file)
2. Write test cases for task
3. Run tests → All should FAIL
4. Commit test code

### GREEN Phase: Implement to Pass Tests
1. Write minimal code to pass tests
2. Run tests → All should PASS
3. Verify no spec/plan deviation
4. Commit implementation code

### REFACTOR Phase: Optimize Code
1. Review code for clarity
2. Refactor within passing tests
3. Run tests → All should still PASS
4. Commit refactored code

### Done Criteria for Each Task
- [ ] Tests written and passing
- [ ] Code matches specification and plan
- [ ] No feature invention
- [ ] No Phase II concepts
- [ ] Docstrings complete
- [ ] Code reviewed

---

## Testing Approach

### Unit Tests (80% of test code)
- Task model creation and methods
- ID generation algorithm
- Validation logic (title, description, ID)
- CRUD operations (isolated from CLI)
- Status transitions
- Error handling (exception raising)

### Integration Tests (20% of test code)
- Multi-feature workflows
- Service and repository integration
- Complete user scenarios
- Error recovery paths

### Manual Testing
- Menu navigation
- User input scenarios
- Error message clarity
- User experience

---

## Phase I Completion Criteria

Phase I is COMPLETE when:

✅ **All Tasks Done**
- All 19 tasks completed
- All tests passing
- Code reviewed

✅ **Specification Met**
- All 5 user stories implemented
- All acceptance criteria satisfied
- All error cases handled
- Data model correct

✅ **Plan Fulfilled**
- Four-layer architecture implemented
- Clean separation of concerns
- Testable design achieved
- No Phase II concepts

✅ **Quality Standards**
- PEP 8 compliant
- Docstrings complete
- Test coverage 80%+
- Code is clean and maintainable

✅ **Constitution Compliant**
- Spec-first development followed
- Clean architecture applied
- No agent behavior violations
- No feature invention

---

**Document Status**: 🟢 READY FOR APPROVAL

**Next Step**: User approves task breakdown, then implementation begins with TASK-001 (Red-Green-Refactor cycle).

---

**Version**: 1.0.0 | **Date**: 2025-12-30 | **Status**: Pending User Approval
