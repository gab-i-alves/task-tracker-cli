import sys
import json
import os
from datetime import datetime
import pyfiglet

def display_title():
    title = pyfiglet.figlet_format("Task Tracker")
    print(title)

TASKS_FILE = "tasks.json"

# Ensure the JSON file exists
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as f:
        f.write("[]")  # Initialize with an empty JSON array


def load_tasks():
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def main():
    display_title()
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "add":
        add_task(args)
    elif command == "update":
        update_task(args)
    elif command == "delete":
        delete_task(args)
    elif command == "mark-in-progress":
        mark_task(args, "in-progress")
    elif command == "mark-done":
        mark_task(args, "done")
    elif command == "list":
        list_tasks(args)
    else:
        print(f"Unknown command: {command}")

def add_task(args):
    if len(args) < 1:
        print("Usage: task-cli add <description>")
        return

    description = args[0]
    tasks = load_tasks()
    task_id = len(tasks) + 1
    now = datetime.now().isoformat()
    tasks.append({
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    })
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def update_task(args):
    if len(args) < 2:
        print("Usage: task-cli update <id> <new_description>")
        return

    task_id = int(args[0])
    new_description = args[1]
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully")
            return

    print(f"Task with ID {task_id} not found")

def delete_task(args):
    if len(args) < 1:
        print("Usage: task-cli delete <id>")
        return

    task_id = int(args[0])
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task with ID {task_id} deleted successfully")

def mark_task(args, status):
    if len(args) < 1:
        print(f"Usage: task-cli mark-{status} <id>")
        return

    task_id = int(args[0])
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return

    print(f"Task with ID {task_id} not found")

def list_tasks(args):
    tasks = load_tasks()

    if not args:
        print("All Tasks:")
        for task in tasks:
            print(task)
        return

    filter_status = args[0]
    filtered_tasks = [task for task in tasks if task["status"] == filter_status]

    if not filtered_tasks:
        print(f"No tasks with status '{filter_status}'")
    else:
        print(f"Tasks with status '{filter_status}':")
        for task in filtered_tasks:
            print(task)


if __name__ == "__main__":
    main()
