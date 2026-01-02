# Evolution of Todo - Phase I

**A simple, in-memory console todo application built with clean architecture principles.**

## Overview

This is Phase I of the Evolution of Todo project: a single-user, in-memory Python console application for managing todo tasks. It provides basic CRUD operations (Create, Read, Update, Delete) through a menu-driven CLI interface.

**Phase I Scope**:
- ✅ In-memory task storage (no database, no files)
- ✅ Menu-driven command-line interface
- ✅ Add, view, update, delete, and toggle task status
- ✅ Basic validation and error handling
- ✅ Clean architecture with separation of concerns

**What's NOT in Phase I**:
- ❌ Database persistence
- ❌ File storage
- ❌ Web interface or API
- ❌ Authentication
- ❌ Real-time features
- ❌ AI integration

## Project Structure

```
app/
├── main.py              # Application entry point
├── __init__.py          # Package initialization
├── models.py            # Domain layer: Task entity
├── repository.py        # Repository layer: In-memory storage
├── service.py           # Service layer: Business logic
├── ui.py               # CLI layer: User interface
└── exceptions.py       # Custom exception classes

tests/
├── test_models.py       # Domain model tests
├── test_repository.py   # Repository tests
├── test_service.py      # Service layer tests
└── test_integration.py  # End-to-end workflow tests

requirements.txt         # Python dependencies
pytest.ini             # Pytest configuration
README.md              # This file
```

## Architecture

The application follows clean architecture with four distinct layers:

### Domain Layer (models.py)
- **Task**: Entity representing a todo item
- **TaskStatus**: Enumeration for task status (INCOMPLETE, COMPLETE)
- Independent of UI and storage details

### Repository Layer (repository.py)
- **TaskRepository**: In-memory storage using Python dictionary
- Manages task persistence and sequential ID generation
- Abstracts storage implementation

### Service Layer (service.py)
- **TaskService**: Business logic and validation
- Coordinates between domain and CLI layers
- Raises typed exceptions for CLI error handling

### CLI Layer (ui.py)
- **TodoApp**: Menu-driven user interface
- Input handling and validation
- Result display and error message formatting

## Running the Application

### Prerequisites
- Python 3.10 or higher
- No external dependencies required (uses Python standard library only)

### Installation
```bash
# Install test dependencies (optional)
pip install -r requirements.txt
```

### Running the Application
```bash
# From the project root directory
python app/main.py
```

The application will start with an interactive menu:

```
========== TODO APPLICATION ==========
Welcome to your Todo application!

========== TODO APPLICATION ==========
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Choose an option (1-6):
```

## Using the Application

### Add a Task
1. Select option `1` from the menu
2. Enter task title (required)
3. Enter task description (optional, press Enter to skip)
4. Task is created and assigned a unique ID

### View Tasks
1. Select option `2` from the menu
2. All tasks are displayed in a formatted table with:
   - Task ID
   - Status (✓ for complete, ○ for incomplete)
   - Title
   - Description
3. Summary shows total, completed, and remaining tasks

### Update a Task
1. Select option `3` from the menu
2. Enter the task ID to update
3. Current task details are displayed
4. Enter new title (press Enter to keep current)
5. Enter new description (press Enter to keep current)
6. Task is updated if changes were made

### Delete a Task
1. Select option `4` from the menu
2. Enter the task ID to delete
3. Confirm deletion (y/n)
4. Task is removed from the list

### Mark Task Complete/Incomplete
1. Select option `5` from the menu
2. Enter the task ID
3. Choose: 1) Mark Complete or 2) Mark Incomplete
4. Task status is toggled

### Exit
1. Select option `6` from the menu
2. Application terminates

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_service.py
```

### Run Tests Verbosely
```bash
pytest -v
```

## Test Coverage

The application includes comprehensive test coverage:

- **Unit Tests**:
  - `test_models.py`: Task entity and TaskStatus enum (100% coverage)
  - `test_repository.py`: Storage operations and ID generation (100% coverage)
  - `test_service.py`: Business logic and validation (100% coverage)

- **Integration Tests**:
  - `test_integration.py`: Complete workflows across multiple features

**Overall Coverage**: 80%+ of application code

## Data Model

### Task Entity

```python
Task:
    id: int                      # Immutable, unique, sequential (1, 2, 3, ...)
    title: str                   # Required, 1-200 characters (mutable)
    description: str             # Optional, 0-500 characters (mutable)
    status: TaskStatus          # INCOMPLETE or COMPLETE (mutable)
    created_at: datetime        # Creation timestamp (immutable)
```

### Task Status
- `INCOMPLETE` (○) - Task is pending
- `COMPLETE` (✓) - Task is done

### ID Generation
- IDs start at 1
- IDs increment sequentially (1, 2, 3, ...)
- IDs are never reused (even after deletion)
- ID gaps are allowed: Delete task 2, next ID is 4 (not 2)

## Validation Rules

### Task Title
- Required (cannot be empty)
- No whitespace-only titles
- Maximum 200 characters
- Leading/trailing whitespace is trimmed

### Task Description
- Optional (can be empty)
- Maximum 500 characters
- Leading/trailing whitespace is trimmed

### Task ID
- Must be numeric
- Must exist in the system
- Cannot be negative or zero

### Confirmation (y/n)
- Case-insensitive
- Accepts: 'y', 'yes', 'n', 'no'

## Error Handling

The application handles errors gracefully:

| Error | Cause | Message |
|-------|-------|---------|
| Invalid Menu | Non-numeric or out-of-range selection | "Please enter a number between 1 and 6" |
| Empty Title | User provides no or whitespace-only title | "Task title cannot be empty" |
| Title Too Long | Title exceeds 200 characters | "Task title exceeds 200 characters" |
| Description Too Long | Description exceeds 500 characters | "Description exceeds 500 characters" |
| Invalid Task ID | Non-numeric input for task ID | "Task ID must be a number" |
| Task Not Found | Task ID doesn't exist | "Task ID X not found" |
| Already Complete | Trying to mark complete→complete | "Task is already complete" |
| Already Incomplete | Trying to mark incomplete→incomplete | "Task is already incomplete" |
| Invalid Confirmation | Non-y/n response | "Please enter 'y' or 'n'" |

All errors are recoverable - the user can retry immediately or return to the main menu.

## Example Workflow

```
$ python app/main.py

========== TODO APPLICATION ==========
Welcome to your Todo application!

========== TODO APPLICATION ==========
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Choose an option (1-6): 1

--- Add Task ---
Enter task title: Buy groceries
Enter task description (press Enter to skip): Milk, eggs, bread
✓ Task created with ID: 1
Task: "Buy groceries" [incomplete]

========== TODO APPLICATION ==========
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Choose an option (1-6): 2

--- Your Tasks ---

ID   Status   Title                 Description
---------------------------------------------------------------------------
1    ○        Buy groceries         Milk, eggs, bread
---------------------------------------------------------------------------
Total: 1 tasks | Completed: 0 | Remaining: 1

========== TODO APPLICATION ==========
Choose an option (1-6): 5

--- Mark Task Complete/Incomplete ---
Enter task ID: 1
Current status: ○ incomplete

1. Mark Complete
2. Mark Incomplete

Choose (1-2): 1
✓ Task 1 marked as complete
New status: ✓ complete

========== TODO APPLICATION ==========
Choose an option (1-6): 6

Goodbye!
```

## Development Guidelines

This application was built following:

1. **Spec-Driven Development**: Every feature is driven by the specification
2. **Test-First Development**: Tests are written before implementation
3. **Clean Architecture**: Clear separation between domain, service, and UI layers
4. **No External Dependencies**: Uses Python standard library only

## Constitutional Alignment

This application fully complies with the Evolution of Todo Global Constitution:

- ✅ Spec-driven development
- ✅ Clean architecture with separation of concerns
- ✅ No unauthorized features
- ✅ Specification-first (no code without spec)
- ✅ Testable design
- ✅ Clear error handling
- ✅ No Phase II+ concepts

## Future Phases

This Phase I foundation will be extended in future phases:

- **Phase II**: REST API with FastAPI
- **Phase III**: Real-time updates with WebSockets/Kafka
- **Phase IV**: AI agents with OpenAI SDK
- **Phase V**: Cloud-native deployment with Kubernetes/Dapr

The architecture is designed to support these extensions without breaking changes to the domain and service layers.

## License

Part of the Evolution of Todo project - Hackathon 2025

---

**For more information**: See the specification and architecture plan in the `specs/phase-1-core-console-app/` directory.
