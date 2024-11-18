import sys
import json
import os
from datetime import datetime
import pyfiglet

# Three classes: Task, TaskManager and TaskCLI

class Task:
    """Represents a single task."""

    # All the attributes
    def __init__(self, task_id, description, status="todo", created_at=None, updated_at=None):
        self.id = task_id
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def to_dict(self):
        """Converts the Task instance to a dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Task instance from a dictionary."""
        return cls(
            task_id=data["id"],
            description=data["description"],
            status=data["status"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"],
        )

class TaskManager:
    """Handles loading, saving, and managing tasks."""

    TASKS_FILE = "tasks.json"

    def __init__(self):
        self.tasks = []
        self._ensure_tasks_file()

    def _ensure_tasks_file(self):
        """Ensures the tasks file exists and initializes it if necessary."""
        if not os.path.exists(self.TASKS_FILE):
            with open(self.TASKS_FILE, "w") as f:
                json.dump([], f)
        self.load_tasks()

    def load_tasks(self):
        """Loads tasks from the JSON file."""
        with open(self.TASKS_FILE, "r") as f:
            task_dicts = json.load(f)
        self.tasks = [Task.from_dict(task) for task in task_dicts]

    def save_tasks(self):
        """Saves tasks to the JSON file."""
        with open(self.TASKS_FILE, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, description):
        """Adds a new task."""
        task_id = len(self.tasks) + 1
        new_task = Task(task_id=task_id, description=description)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Task added successfully (ID: {task_id})")

    def update_task(self, task_id, new_description):
        """Updates the description of an existing task."""
        task = self._find_task_by_id(task_id)
        if task:
            task.description = new_description
            task.updated_at = datetime.now().isoformat()
            self.save_tasks()
            print(f"Task {task_id} updated successfully")
        else:
            print(f"Task with ID {task_id} not found")

    def delete_task(self, task_id):
        """Deletes a task by ID."""
        task = self._find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Task with ID {task_id} not found")

    def mark_task(self, task_id, status):
        """Marks a task as a specific status."""
        task = self._find_task_by_id(task_id)
        if task:
            task.status = status
            task.updated_at = datetime.now().isoformat()
            self.save_tasks()
            print(f"Task {task_id} marked as {status}")
        else:
            print(f"Task with ID {task_id} not found")

    def list_tasks(self, status=None):
        """Lists tasks, optionally filtered by status."""
        filtered_tasks = self.tasks if not status else [task for task in self.tasks if task.status == status]
        if filtered_tasks:
            for task in filtered_tasks:
                print(f"ID: {task.id}, Description: {task.description}, Status: {task.status}")
        else:
            print("No tasks found" + (f" with status '{status}'" if status else ""))

    def _find_task_by_id(self, task_id):
        """Finds a task by its ID."""
        return next((task for task in self.tasks if task.id == task_id), None)


class TaskCLI:
    """CLI interface for interacting with the Task Manager."""

    def __init__(self):
        self.manager = TaskManager()

    def display_title(self):
        """Displays the title of the CLI."""
        title = pyfiglet.figlet_format("Task Tracker")
        print(title)

    def handle_command(self, args):
        """Parses and executes CLI commands."""
        if not args:
            print("Usage: task-cli <command> [arguments]")
            return

        command = args[0]
        params = args[1:]

        if command == "add" and params:
            self.manager.add_task(params[0])
        elif command == "update" and len(params) >= 2:
            self.manager.update_task(int(params[0]), params[1])
        elif command == "delete" and len(params) >= 1:
            self.manager.delete_task(int(params[0]))
        elif command == "mark-in-progress" and len(params) >= 1:
            self.manager.mark_task(int(params[0]), "in-progress")
        elif command == "mark-done" and len(params) >= 1:
            self.manager.mark_task(int(params[0]), "done")
        elif command == "list":
            self.manager.list_tasks(params[0] if params else None)
        else:
            print(f"Unknown command or incorrect usage: {command}")


def main():
    cli = TaskCLI()
    cli.display_title()
    cli.handle_command(sys.argv[1:])


if __name__ == "__main__":
    main()
