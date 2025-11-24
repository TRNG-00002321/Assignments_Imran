import json
from pathlib import Path

DATA_FILE = Path("todos.json")

def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def add_task(tasks):
    title = input("Task title: ").strip()
    if not title:
        print("No title entered.")
        return
    task = {"title": title, "completed": False}
    tasks.append(task)
    save_tasks(tasks)
    print("Added.")

def view_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return
    for i, t in enumerate(tasks, start=1):
        status = "✔" if t.get("completed") else "✗"
        print(f"{i}. [{status}] {t.get('title')}")

def complete_task(tasks):
    if not tasks:
        print("No tasks to complete.")
        return
    view_tasks(tasks)
    try:
        n = int(input("Mark which task number as complete? ")) - 1
    except ValueError:
        print("Enter a number.")
        return
    if 0 <= n < len(tasks):
        tasks[n]["completed"] = True
        save_tasks(tasks)
        print("Marked complete.")
    else:
        print("Invalid number.")

def delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return
    view_tasks(tasks)
    try:
        n = int(input("Delete which task number? ")) - 1
    except ValueError:
        print("Enter a number.")
        return
    if 0 <= n < len(tasks):
        removed = tasks.pop(n)
        save_tasks(tasks)
        print(f"Deleted: {removed.get('title')}")
    else:
        print("Invalid number.")

def main():
    tasks = load_tasks()
    while True:
        print("\n1) Add task\n2) View tasks\n3) Mark complete\n4) Delete task\n5) Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
