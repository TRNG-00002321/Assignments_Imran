from flask import Flask, request, redirect, url_for, render_template
import json
from pathlib import Path

# --- Configuration ---
app = Flask(__name__)
DATA_FILE = Path("todos.json")


# --- Utility Functions for Data Persistence ---

def load_tasks():
    """Loads tasks from the JSON file. Returns an empty list if the file is missing or invalid."""
    if not DATA_FILE.exists():
        # Initialize with an empty list if the file doesn't exist
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure the loaded data is a list
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError:
        # Handle empty or corrupted JSON file
        return []
    except Exception:
        # Catch other potential file errors
        return []


def save_tasks(tasks):
    """Saves the current list of tasks to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


# --- View Routes ---

@app.route("/")
def home():
    """Displays the list of all To-Do tasks."""
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    """Handles adding a new task from a form submission."""
    title = request.form.get("title", "").strip()
    if title:
        tasks = load_tasks()
        tasks.append({"title": title, "completed": False})
        save_tasks(tasks)
    return redirect(url_for("home"))


@app.route("/complete/<int:idx>", methods=["POST"])
def complete(idx):
    """Marks a task as completed based on its index."""
    tasks = load_tasks()
    # Check if the index is valid
    if 0 <= idx < len(tasks):
        tasks[idx]["completed"] = True
        save_tasks(tasks)
    return redirect(url_for("home"))


@app.route("/delete/<int:idx>", methods=["POST"])
def delete(idx):
    """Deletes a task based on its index."""
    tasks = load_tasks()
    # Check if the index is valid
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        save_tasks(tasks)
    return redirect(url_for("home"))


# --- New Edit/Update Functionality ---

@app.route("/edit/<int:idx>")
def edit_task(idx):
    """
    Shows the form for editing an existing task.
    Requires a 'templates/edit.html' file.
    """
    tasks = load_tasks()
    if 0 <= idx < len(tasks):
        task = tasks[idx]
        # Pass the task and its index to the template for display
        return render_template("edit.html", task=task, index=idx)

    # Redirect if the index is invalid
    return redirect(url_for("home"))


@app.route("/update/<int:idx>", methods=["POST"])
def update(idx):
    """
    Handles the form submission to update a task's title.
    """
    new_title = request.form.get("title", "").strip()

    # Only proceed if we received a non-empty title
    if new_title:
        tasks = load_tasks()
        # Check if the index is valid
        if 0 <= idx < len(tasks):
            # Update the title of the specific task at the given index
            tasks[idx]["title"] = new_title
            save_tasks(tasks)

    # Redirect back to the main list after update
    return redirect(url_for("home"))


# --- Run Application ---
if __name__ == "__main__":
    app.run(debug=True)