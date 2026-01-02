# Phase I: Core Console Todo Application - Specification

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Phase**: I (Foundation)

**Constitutional Alignment**: ✅ Complies with EVOLUTION_CONSTITUTION.md Part I, III, IV, V

---

## 1. Overview

### Project Statement
Build a single-user, in-memory console application for todo task management with basic CRUD operations. This is the foundation phase establishing core domain logic and user interaction patterns before any persistence or architecture complexity is introduced.

### Phase I Scope
- **Technology**: Python 3.10+ (console application)
- **Runtime**: Single user, single session
- **Data**: In-memory only (no persistence, no files, no database)
- **Interface**: Text-based CLI with menu-driven interaction
- **Complexity**: Basic level only (no advanced features)

### What Phase I Is NOT
- ❌ Not a REST API (Phase II+)
- ❌ Not persistent storage (Phase II+)
- ❌ Not authenticated (Phase II+)
- ❌ Not web-based (Phase II+)
- ❌ Not real-time (Phase III+)
- ❌ Not AI-powered (Phase IV+)
- ❌ Not distributed (Phase V+)

### Success Criteria
- ✅ All basic CRUD operations working correctly
- ✅ User can manage todos via CLI menu
- ✅ All error cases handled gracefully
- ✅ Data structures match specification exactly
- ✅ Test coverage minimum 80%
- ✅ Application runs without external dependencies (console only)

---

## 2. User Stories

Each user story defines a single, testable capability aligned to Phase I scope.

### Story 1: Add a New Task

**As a** user
**I want to** add a new task to my todo list
**So that** I can track things I need to do

**Acceptance Criteria**:
- [ ] User can input a task title
- [ ] User can input a task description (optional)
- [ ] Task is created with a unique ID (auto-generated)
- [ ] Task defaults to "incomplete" status
- [ ] Task is stored in memory and accessible immediately
- [ ] Confirmation message shows new task ID
- [ ] System handles empty or whitespace-only titles (error)

**Example Flow**:
```
Menu: > [1] Add Task
Enter task title: "Buy groceries"
Enter task description (press Enter to skip): "Milk, eggs, bread"
✓ Task created with ID: 1
Task: "Buy groceries" [incomplete]
```

**Error Cases**:
- Empty task title → "Error: Task title cannot be empty"
- Only whitespace → "Error: Task title cannot be empty"
- Recoverable: User can retry immediately

---

### Story 2: View Task List

**As a** user
**I want to** see all my tasks in a formatted list
**So that** I can review everything I need to do

**Acceptance Criteria**:
- [ ] User can view all tasks in the system
- [ ] Tasks are displayed with: ID, Title, Description, Status
- [ ] Status shows "✓ complete" or "○ incomplete"
- [ ] Tasks are displayed in ID order (ascending)
- [ ] List shows count of total tasks
- [ ] Empty list shows: "No tasks yet"
- [ ] List is readable and well-formatted

**Example Flow**:
```
Menu: > [2] View Tasks
========== YOUR TASKS ==========
ID | Status | Title              | Description
---+--------+--------------------+-------------------
1  | ○      | Buy groceries      | Milk, eggs, bread
2  | ✓      | Call dentist       | (no description)
3  | ○      | Finish project     | Due Friday
================================
Total: 3 tasks | Completed: 1 | Remaining: 2
```

**Error Cases**:
- No tasks in list → Display "No tasks yet" (not an error)

---

### Story 3: Update Task

**As a** user
**I want to** update a task's title or description
**So that** I can fix mistakes or add more details

**Acceptance Criteria**:
- [ ] User can select a task by ID
- [ ] User can update title (optional field)
- [ ] User can update description (optional field)
- [ ] User can update neither (no change)
- [ ] Original task ID remains the same
- [ ] Task status is not changed by update
- [ ] Confirmation shows updated task details
- [ ] Invalid task ID shows error

**Example Flow**:
```
Menu: > [3] Update Task
Enter task ID to update: 1
Current task: "Buy groceries" (Milk, eggs, bread)

Enter new title (press Enter to keep current): "Get groceries"
Enter new description (press Enter to keep current): "Milk, eggs, bread, cheese"

✓ Task 1 updated successfully
Updated task: "Get groceries" (Milk, eggs, bread, cheese)
```

**Error Cases**:
- Task ID not found → "Error: Task ID 99 not found"
- Non-numeric ID → "Error: Task ID must be a number"
- No changes → "No changes made. Task remains unchanged"

---

### Story 4: Delete Task

**As a** user
**I want to** delete a task I no longer need
**So that** I can remove items from my list

**Acceptance Criteria**:
- [ ] User can delete a task by ID
- [ ] Deleted task is removed from memory
- [ ] Remaining tasks keep their IDs (gaps are allowed)
- [ ] Confirmation shows deleted task details
- [ ] Invalid task ID shows error
- [ ] Cannot delete non-existent task

**Example Flow**:
```
Menu: > [4] Delete Task
Enter task ID to delete: 2
Delete task? "Call dentist" (no description) [y/n]: y

✓ Task 2 deleted successfully
```

**Error Cases**:
- Task ID not found → "Error: Task ID 99 not found"
- Non-numeric ID → "Error: Task ID must be a number"
- User cancels deletion → "Deletion cancelled. Task remains"

---

### Story 5: Mark Task Complete

**As a** user
**I want to** mark a task as complete
**So that** I can track my progress

**Acceptance Criteria**:
- [ ] User can mark a task as complete by ID
- [ ] Task status changes to "complete"
- [ ] Task can be unmarked (set to incomplete)
- [ ] Only incomplete tasks can be marked complete
- [ ] Only complete tasks can be marked incomplete
- [ ] Original task data is preserved
- [ ] Confirmation shows updated status

**Example Flow**:
```
Menu: > [5] Mark Task Complete/Incomplete
Enter task ID: 1
Current status: ○ incomplete

Toggle status? (1: Mark Complete, 2: Mark Incomplete): 1
✓ Task 1 marked as complete
New status: ✓ complete
```

**Error Cases**:
- Task ID not found → "Error: Task ID 99 not found"
- Non-numeric ID → "Error: Task ID must be a number"
- Already complete, trying to mark complete → "Error: Task is already complete"
- Already incomplete, trying to mark incomplete → "Error: Task is already incomplete"

---

## 3. Task Data Model

### Task Entity

```
class Task:
    id: int                    # Auto-generated, unique, sequential
    title: str                 # Required, non-empty, max 200 chars
    description: str           # Optional, max 500 chars
    status: TaskStatus         # Either "complete" or "incomplete"
    created_at: datetime       # Timestamp of creation (ISO 8601)
```

### Data Constraints

| Field | Type | Required | Min | Max | Default | Constraints |
|-------|------|----------|-----|-----|---------|------------|
| id | int | Yes | N/A | N/A | Auto-increment | Unique, sequential from 1 |
| title | str | Yes | 1 char | 200 chars | N/A | Non-empty, no leading/trailing spaces |
| description | str | No | 0 chars | 500 chars | Empty string | Optional |
| status | enum | Yes | N/A | N/A | "incomplete" | "complete" or "incomplete" |
| created_at | datetime | Yes | N/A | N/A | Now | ISO 8601 format |

### Task Status Enum

```
TaskStatus = Enum
  - "complete"     ✓ Task is done
  - "incomplete"   ○ Task is pending
```

### Task ID Generation

- IDs start at 1
- IDs increment sequentially
- IDs are never reused (even after deletion)
- Next available ID = max(existing IDs) + 1

### In-Memory Storage

```
tasks: Dict[int, Task]
  - Key: task ID (int)
  - Value: Task instance
  - Data structure: Python dictionary
```

---

## 4. CLI Interaction Flow

### Main Menu

```
========== TODO APPLICATION ==========
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Choose an option (1-6):
```

### Interaction Patterns

#### Pattern 1: Menu Selection
- User enters number (1-6)
- Invalid input → show error, repeat menu
- Valid selection → execute action

#### Pattern 2: Task Input
- Prompt user for task title
- Prompt user for task description (optional)
- Validate input
- Create task
- Show confirmation

#### Pattern 3: Task Selection
- Prompt for task ID
- Validate ID is numeric
- Validate ID exists
- Execute action

#### Pattern 4: Confirmation
- Ask user to confirm destructive actions (delete, toggle)
- User enters y/n
- Invalid input → repeat prompt
- Execute only on y

### User Input Validation

All user input must be validated:

1. **Menu Selection**
   - Must be 1-6
   - Must be numeric
   - "Error: Please enter a number between 1 and 6"

2. **Task Title**
   - Must be non-empty
   - Must not be only whitespace
   - Max 200 characters
   - "Error: Task title cannot be empty"
   - "Error: Task title exceeds 200 characters"

3. **Task Description**
   - Optional (can be empty)
   - Max 500 characters
   - "Error: Description exceeds 500 characters"

4. **Task ID**
   - Must be numeric
   - Must exist in system
   - "Error: Task ID must be a number"
   - "Error: Task ID 99 not found"

5. **Confirmation (y/n)**
   - Must be y or n
   - Case-insensitive
   - "Error: Please enter 'y' or 'n'"

### Session Lifecycle

1. **Start**: Application launches, empty task list
2. **Loop**: Show menu, accept input, execute action, return to menu
3. **Exit**: User selects "Exit" or sends EOF (Ctrl+D / Ctrl+Z)
4. **End**: Application terminates, in-memory data is lost

---

## 5. Acceptance Criteria by Feature

### Feature 1: Add Task

- [ ] New task can be created with title only
- [ ] New task can be created with title and description
- [ ] Auto-generated ID is unique and sequential
- [ ] New task defaults to "incomplete" status
- [ ] Task is immediately accessible via View or Update
- [ ] Empty title is rejected with error
- [ ] Whitespace-only title is rejected with error
- [ ] Title longer than 200 chars is rejected with error
- [ ] Description longer than 500 chars is rejected with error
- [ ] Confirmation message displays task ID and title

### Feature 2: View Tasks

- [ ] All tasks are displayed in ascending ID order
- [ ] Each task shows ID, Status, Title, Description
- [ ] Status displays as "✓ complete" or "○ incomplete"
- [ ] Empty list shows "No tasks yet"
- [ ] Summary line shows total tasks, completed, remaining
- [ ] List is properly formatted and readable
- [ ] List updates immediately after add/update/delete/toggle

### Feature 3: Update Task

- [ ] User can update title only
- [ ] User can update description only
- [ ] User can update both title and description
- [ ] User can skip updates (no change)
- [ ] Task ID is never changed
- [ ] Task status is never changed by update
- [ ] Invalid task ID shows error and returns to menu
- [ ] Updated task is immediately reflected in View

### Feature 4: Delete Task

- [ ] User can delete a task that exists
- [ ] Deleted task is removed from all operations
- [ ] Task ID gaps are allowed (after deletion)
- [ ] Cannot delete non-existent task ID
- [ ] User must confirm before deletion
- [ ] Canceling deletion leaves task unchanged
- [ ] Confirmation message shows deleted task details

### Feature 5: Mark Task Complete/Incomplete

- [ ] Complete task can be marked as incomplete
- [ ] Incomplete task can be marked as complete
- [ ] Cannot mark complete task as complete
- [ ] Cannot mark incomplete task as incomplete
- [ ] Task title and description unchanged by toggle
- [ ] Toggle is immediately reflected in View
- [ ] Invalid task ID shows error
- [ ] Confirmation message shows new status

---

## 6. Error Cases & Handling

### Error Taxonomy

| Error Type | Cause | Message | User Can Retry |
|-----------|-------|---------|-----------------|
| Invalid Menu Input | User enters non-numeric or out-of-range | "Please enter a number between 1 and 6" | Yes |
| Empty Task Title | User provides empty or whitespace-only title | "Task title cannot be empty" | Yes |
| Title Too Long | Title exceeds 200 characters | "Task title exceeds 200 characters" | Yes |
| Description Too Long | Description exceeds 500 characters | "Description exceeds 500 characters" | Yes |
| Invalid Task ID | User enters non-numeric task ID | "Task ID must be a number" | Yes |
| Task Not Found | Task ID doesn't exist | "Task ID [ID] not found" | Yes |
| Already Complete | User tries to mark complete task as complete | "Task is already complete" | No |
| Already Incomplete | User tries to mark incomplete task as incomplete | "Task is already incomplete" | No |
| Invalid Confirmation | User enters non-y/n response | "Please enter 'y' or 'n'" | Yes |

### Error Handling Behavior

1. **Input Validation Errors**: Show error message, repeat same prompt
2. **Logic Errors**: Show error message, return to main menu
3. **Recoverable Errors**: Allow user to retry immediately
4. **Data Integrity**: System should never enter invalid state

### Error Message Format

```
Error: [Specific error message]
[Optional: Action to take]
```

Example:
```
Error: Task title cannot be empty
Please try again or choose another option.
```

---

## 7. Out of Scope (NOT Phase I)

The following features and concepts are **explicitly excluded** from Phase I:

### Database & Persistence
- ❌ File storage (.txt, .json, .csv)
- ❌ Database connections (SQL, NoSQL)
- ❌ Permanent data retention across sessions
- ❌ Data backup or recovery

### Authentication & Security
- ❌ User login/logout
- ❌ Password hashing
- ❌ Authorization or roles
- ❌ Data encryption
- ❌ Audit logging

### Network & APIs
- ❌ REST API endpoints
- ❌ HTTP server
- ❌ WebSocket connections
- ❌ Network communication

### Advanced Features
- ❌ Task categories or tags
- ❌ Priorities or due dates
- ❌ Task dependencies
- ❌ Recurring tasks
- ❌ Search or filtering
- ❌ Sorting options
- ❌ Undo/redo functionality
- ❌ Task assignment or sharing

### Real-Time & Streaming
- ❌ Real-time updates
- ❌ Event streaming
- ❌ Message queues

### AI & Intelligence
- ❌ Task suggestions
- ❌ Natural language processing
- ❌ AI classification

### Cloud & Deployment
- ❌ Docker containerization
- ❌ Cloud deployment
- ❌ Kubernetes orchestration
- ❌ Microservices architecture

---

## 8. Non-Functional Requirements

### Performance
- **Response Time**: User actions should complete in <100ms
- **Memory Usage**: Application should use <50MB RAM
- **Scalability**: Support up to 1000 tasks in-memory
- **No latency concerns**: Single-user, single-threaded

### Reliability
- **Availability**: Application runs without external dependencies
- **Data Integrity**: No data corruption in memory
- **Crash Recovery**: Not applicable (no persistence)
- **Uptime**: Not applicable (single session)

### Usability
- **Clarity**: User prompts are clear and unambiguous
- **Feedback**: User receives confirmation after actions
- **Error Recovery**: Errors are recoverable without restart
- **Help**: Menu is always available

### Code Quality
- **Test Coverage**: Minimum 80%
- **Code Style**: PEP 8 compliant
- **Documentation**: Docstrings for all functions
- **Clean Architecture**: Domain logic separated from UI

---

## 9. Test Strategy

### Unit Tests

Test individual functions in isolation:

**Task Model Tests**:
- Create task with title only
- Create task with title and description
- Task defaults to incomplete status
- Auto-generated IDs are sequential
- Task ID cannot be duplicated

**Task Service Tests**:
- Add valid task
- Add task with empty title (rejection)
- Add task with long title (rejection)
- View empty list
- View task list with multiple tasks
- View tasks in ID order
- Update task title
- Update task description
- Update both fields
- Delete existing task
- Delete non-existent task (error)
- Mark task complete
- Mark task incomplete
- Mark already-complete as complete (error)

### Integration Tests

Test workflows across multiple features:

**Workflow Tests**:
- Add → View (task appears)
- Add → Update → View (changes appear)
- Add → Delete → View (task disappears)
- Add → Mark Complete → View (status updated)
- Multiple adds → View (order is correct)
- Update → Mark Complete (both operations work)

### Manual Testing

Test user interaction scenarios:

**Scenario Tests**:
- User navigates menu correctly
- User can handle invalid menu selection
- User can recover from input errors
- User can complete full workflow (add, view, update, delete, toggle)
- Empty list shows appropriate message
- Confirmation dialogs work correctly

### Coverage Target
- **Minimum**: 80% code coverage
- **Focus Areas**:
  - Task creation and ID generation (100%)
  - Input validation (100%)
  - Error handling (100%)
  - Status transitions (100%)

---

## 10. API Contract (Data Model Only)

**Note**: Phase I is a console application with no REST API. This section documents the data model contract that will be formalized as API in Phase II+.

### Task Representation

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "incomplete",
  "created_at": "2025-12-30T10:30:00Z"
}
```

### Operations

| Operation | Input | Output | Error |
|-----------|-------|--------|-------|
| Create Task | title, description? | Task (with ID) | Invalid input |
| Read Tasks | (none) | List[Task] | (none) |
| Read Task | id | Task | Not found |
| Update Task | id, title?, description? | Task (updated) | Not found |
| Delete Task | id | (confirmation) | Not found |
| Toggle Status | id | Task (updated) | Not found |

---

## 11. Constraints & Assumptions

### Constraints

1. **Single User**: No multi-user support or concurrency
2. **In-Memory Only**: No persistence, no files, no database
3. **Console Only**: Text input/output, no GUI
4. **Single Session**: Data is lost when application exits
5. **Python**: Use Python 3.10+ only
6. **No External Dependencies**: Standard library only (except test framework)
7. **Linear ID Generation**: IDs start at 1, increment sequentially

### Assumptions

1. User provides valid task titles (non-empty, reasonable length)
2. User understands CLI interaction patterns
3. Application runs on a system with console support
4. No concurrent access (single-threaded)
5. Task count won't exceed 1000 items

---

## 12. Success Definition

Phase I is complete when:

✅ **All Features Working**
- Add Task: User can create new tasks
- View Tasks: User can list all tasks
- Update Task: User can modify task details
- Delete Task: User can remove tasks
- Toggle Status: User can mark tasks complete/incomplete

✅ **All Acceptance Criteria Met**
- Every criterion in section 5 is satisfied
- Tests verify each acceptance criterion
- Code matches specification exactly

✅ **Error Handling Complete**
- All error cases from section 6 are handled
- Error messages are clear
- User can recover from all errors

✅ **Data Model Correct**
- Task fields match section 3
- Task IDs are sequential and unique
- In-memory storage works correctly

✅ **Tests Passing**
- Unit tests pass (80%+ coverage)
- Integration tests pass
- Manual testing confirms workflow

✅ **Code Quality**
- PEP 8 compliant
- Docstrings on all functions
- Clean code structure

---

## Compliance Checklist

- ✅ Constitutional alignment: EVOLUTION_CONSTITUTION.md Part I (Spec-First)
- ✅ Phase boundaries: Only Phase I features (no Phase II+ features)
- ✅ Technology stack: Python console application (no databases, APIs, etc.)
- ✅ Quality principles: Clean code, test-first, error handling
- ✅ Scope definition: Clear in-scope and out-of-scope boundaries
- ✅ Acceptance criteria: Measurable, testable, objective

---

**Document Status**: 🟢 READY FOR APPROVAL

**Next Steps After Approval**:
1. User approves this specification
2. Create `phase-1-core-console-app/plan.md` (architecture decisions)
3. Create `phase-1-core-console-app/tasks.md` (testable work breakdown)
4. Begin Red-Green-Refactor implementation cycle

---

**Version**: 1.0.0 | **Date**: 2025-12-30 | **Author**: Agent | **Status**: Pending User Approval
