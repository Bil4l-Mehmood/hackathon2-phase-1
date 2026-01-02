"""
CLI layer: User interface and menu-driven interaction.

This module implements the TodoApp class which provides a menu-driven console
interface for the Todo application. Separates user interaction from business logic.
"""

from typing import Optional

try:
    from app.models import TaskStatus
    from app.service import TaskService
    from app.repository import TaskRepository
    from app.exceptions import ValidationError, TaskNotFoundError
except ModuleNotFoundError:
    from models import TaskStatus
    from service import TaskService
    from repository import TaskRepository
    from exceptions import ValidationError, TaskNotFoundError


class TodoApp:
    """
    Command-line interface for Todo application.

    Handles user interaction, menu display, and input handling.
    Translates user input to service calls and displays results.
    """

    def __init__(self) -> None:
        """Initialize CLI with repository and service."""
        self.repo = TaskRepository()
        self.service = TaskService(self.repo)

    def run(self) -> None:
        """Start the application main loop."""
        print("\n========== TODO APPLICATION ==========")
        print("Welcome to your Todo application!\n")

        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 6:  # Exit
                print("\nGoodbye!")
                break

            try:
                self.execute_action(choice)
            except (ValidationError, TaskNotFoundError) as e:
                print(f"\nError: {str(e)}")
            except Exception as e:
                print(f"\nUnexpected error: {str(e)}")

            print()  # Blank line for readability

    # --- Menu Management ---

    def show_menu(self) -> None:
        """Display main menu with all options."""
        print("========== TODO APPLICATION ==========")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print()

    def get_menu_choice(self) -> int:
        """
        Get and validate menu selection from user.

        Returns:
            Valid menu choice (1-6)
        """
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
        """
        Execute selected action based on menu choice.

        Args:
            choice: Menu choice (1-6)
        """
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
        max_length: Optional[int] = None,
    ) -> str:
        """
        Get user text input with optional validation.

        Args:
            prompt: Prompt to display to user
            required: If True, input cannot be empty
            max_length: Maximum allowed length (optional)

        Returns:
            User's input string
        """
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
        """
        Get numeric input from user.

        Args:
            prompt: Prompt to display

        Returns:
            User's numeric input
        """
        while True:
            try:
                value = input(prompt).strip()
                return int(value)
            except ValueError:
                print("Error: Task ID must be a number")

    def get_confirmation(self) -> bool:
        """
        Get y/n confirmation from user.

        Returns:
            True if user confirmed (y/yes), False if declined (n/no)
        """
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
        """Action: Add a new task to the list."""
        print("\n--- Add Task ---")
        title = self.get_text_input("Enter task title: ", required=True)
        description = self.get_text_input(
            "Enter task description (press Enter to skip): ", required=False
        )

        task = self.service.add_task(title, description)

        print(f"✓ Task created with ID: {task.id}")
        print(f"Task: \"{task.title}\" [{task.status.value}]")

    def action_view_tasks(self) -> None:
        """Action: View all tasks in formatted list."""
        print("\n--- Your Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks yet")
            return

        # Display header
        print(f"\n{'ID':<4} {'Status':<8} {'Title':<25} {'Description':<30}")
        print("-" * 70)

        # Display tasks
        for task in tasks:
            status_symbol = "✓" if task.is_complete() else "○"
            desc_display = task.description if task.description else "(no description)"
            # Truncate long descriptions
            if len(desc_display) > 30:
                desc_display = desc_display[:27] + "..."
            print(
                f"{task.id:<4} {status_symbol:<8} "
                f"{task.title:<25} {desc_display:<30}"
            )

        print("-" * 70)

        # Display summary
        total, completed, remaining = self.service.get_statistics()
        print(
            f"Total: {total} tasks | "
            f"Completed: {completed} | "
            f"Remaining: {remaining}\n"
        )

    def action_update_task(self) -> None:
        """Action: Update a task's title and/or description."""
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
            "Enter new title (press Enter to keep current): ", required=False
        )
        new_description = self.get_text_input(
            "Enter new description (press Enter to keep current): ", required=False
        )

        # Use None to indicate "no change"
        updated_task, was_changed = self.service.update_task(
            task_id,
            new_title if new_title else None,
            new_description if new_description != "" else None,
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
        """Action: Delete a task from the list."""
        print("\n--- Delete Task ---")
        task_id = self.get_numeric_input("Enter task ID to delete: ")

        task = self.service.get_task(task_id)
        print(f"Delete task? \"{task.title}\"", end="")
        if task.description:
            print(f" ({task.description})")
        else:
            print()

        if self.get_confirmation():
            deleted_task = self.service.delete_task(task_id)
            print(f"✓ Task {task_id} deleted successfully")
        else:
            print("Deletion cancelled. Task remains")

    def action_toggle_status(self) -> None:
        """Action: Mark task complete or incomplete."""
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
