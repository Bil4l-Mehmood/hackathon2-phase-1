"""
Main entry point for the Todo application.

Run this file to start the application:
    python -m app.main
    or
    python app/main.py
"""

try:
    from app.ui import TodoApp
except ModuleNotFoundError:
    from ui import TodoApp


def main() -> None:
    """Start the Todo application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
