#!/usr/bin/env python
# Shebang line: tells the OS to run this file with the system Python interpreter when executed directly.
"""Django's command-line utility for administrative tasks.

This module provides a small entrypoint used by the project's manage.py script
to run Django administrative commands such as running the development server,
making migrations, or running tests. Each non-blank line below is commented
to explain what it does.
"""

import os  # Import the `os` module to interact with environment variables and filesystem paths.
import sys  # Import the `sys` module to access command-line arguments (sys.argv).


def main():
    """Main entry point for administrative tasks.

    This function sets up the Django settings module environment variable and
    invokes Django's command-line execution helper. Errors during import are
    caught and re-raised with a helpful message.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe.settings')
    # Ensure the DJANGO_SETTINGS_MODULE environment variable is set to the
    # project's settings module used by Django.
    try:
        from django.core.management import execute_from_command_line
        # Import Django's helper to run commands like 'runserver' and 'migrate'.
    except ImportError as exc:
        # If Django isn't installed or import fails, raise a clearer error.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    # Execute the command-line utility with the current process arguments.


if __name__ == '__main__':
    # If this file is executed as a script, call main() to run commands.
    main()
